"""
Client side code to perform a single API call to a tensorflow model up and running.
"""
import argparse
import json

import numpy as np
import requests
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import plot_util
from PIL import Image


def pre_process(image_path):
    """
    Pre-process the input image to return a json to pass to the tf model

    Args:
        image_path (str):  Path to the jpeg image

    Returns:
        formatted_json_input (str)
    """

    image = Image.open(image_path).convert("RGB")
    image_np = plot_util.load_image_into_numpy_array(image)

    # Expand dims to create  bach of size 1
    image_tensor = np.expand_dims(image_np, 0)
    formatted_json_input = json.dumps({"signature_name": "serving_default", "instances": image_tensor.tolist()})

    return formatted_json_input


def post_process(server_response):
    """
    Post-process the server response

    Args:
        server_response (requests.Response)

    Returns:
        post_processed_data (dict)
    """
    response = json.loads(server_response.text)
    post_processed_data = response['predictions'][0]

    # post process classes
    detections_classes = post_processed_data['detection_classes']
    formatted_detection_classes = [int(class_id) for class_id in detections_classes]
    post_processed_data['detection_classes'] = formatted_detection_classes

    # post process num detections
    post_processed_data['num_detections'] = int(post_processed_data['num_detections'])
    return post_processed_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performs call to the tensorflow-serving REST API.')
    parser.add_argument('--server_url', dest='server_url', type=str, required=True,
                        help='URL of the tensorflow-serving accepting API call. '
                             'e.g. http://localhost:8501/v1/models/omr_500:predict')
    parser.add_argument('--image_path', dest='image_path', type=str,
                        help='Path to the jpeg image')
    parser.add_argument('--output_json', dest='output_json', type=str, default='tf_output.json',
                        help='Path to the output json file resulting from the API call')
    parser.add_argument('--save_output_image', dest='save_output_image', type=bool, default=False,
                        help='Whether the output_image should be built from the predictions')
    parser.add_argument('--label_map', dest='label_map', type=str, default="mapping_all_classes.txt",
                        help='Path to the label map, which is json-file that maps each category name '
                             'to a unique number.')
    args = parser.parse_args()

    # Map args to var
    server_url = args.server_url
    image_path = args.image_path
    output_image = args.output_json
    save_output_image = args.save_output_image
    path_to_labels = args.label_map

    # Build input data
    print(f'\n\nPre-processing input file {image_path}...\n')
    formatted_json_input = pre_process(image_path)
    print('Pre-processing done! \n')

    # Call tensorflow server
    headers = {"content-type": "application/json"}
    print(f'\n\nMaking request to {server_url}...\n')
    server_response = requests.post(server_url, data=formatted_json_input, headers=headers)
    print(f'Request returned\n')

    # Post process output
    print(f'\n\nPost-processing server response...\n')
    post_processed_data = post_process(server_response)
    print(f'Post-processing done!\n')

    # Save output on disk
    print(f'\n\nSaving output to {output_image}\n\n')
    with open(output_image, 'w+') as outfile:
        json.dump(post_processed_data, outfile)
    print(f'Output saved!\n')

    if save_output_image:
        # Save output on disk
        print('\n\nBuilding output image\n\n')
        image = Image.open(image_path).convert("RGB")
        image_np = plot_util.load_image_into_numpy_array(image)

        category_index = plot_util.load_category_index(path_to_labels, 99999)  # FIXME: Magic number to replace by meaningful var

        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.array(post_processed_data['detection_boxes']),  # NOTE: np.array needed for .shape property
            post_processed_data['detection_classes'],
            post_processed_data['detection_scores'],
            category_index,
            instance_masks=post_processed_data.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=2,
        )

        output_with_no_extension = output_image.split('.', 1)[0]
        output_image = ''.join([output_with_no_extension, '.jpeg'])
        Image.fromarray(image_np).save(output_image)
        print('\n\nImage saved\n\n')