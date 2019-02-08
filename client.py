"""
Client side code to perform a single API call to a tensorflow model up and running.
"""
import argparse
import json

import numpy as np
import requests
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import plot_util
from object_detection.utils import label_map_util
import object_detection.utils.ops as utils_ops
from PIL import Image

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


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
    output_dict = response['predictions'][0]

    # all outputs are float32 numpy arrays, so convert types as appropriate

    output_dict['num_detections'] = int(output_dict['num_detections'])
    output_dict['detection_classes'] = np.array([int(class_id) for class_id in output_dict['detection_classes']])
    output_dict['detection_boxes'] = np.array(output_dict['detection_boxes'])
    output_dict['detection_scores'] = np.array(output_dict['detection_scores'])

    # Process detection mask
    if 'detection_masks' in output_dict:
        # Determine a threshold above wihc we consider the pixel shall belong to the mask
        # thresh = 0.5
        output_dict['detection_masks'] = np.array(output_dict['detection_masks'])
    return output_dict


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
    output_dict = post_process(server_response)
    print(f'Post-processing done!\n')

    # Save output on disk
    print(f'\n\nSaving output to {output_image}\n\n')
    with open(output_image, 'w+') as outfile:
        json.dump(json.loads(server_response.text), outfile)
    print(f'Output saved!\n')

    if save_output_image:
        # Save output on disk
        print('\n\nBuilding output image\n\n')
        image = Image.open(image_path).convert("RGB")
        image_np = load_image_into_numpy_array(image)

        category_index = label_map_util.create_category_index_from_labelmap(path_to_labels, use_display_name=True)

        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=8,
            )
        output_with_no_extension = output_image.split('.', 1)[0]
        output_image = ''.join([output_with_no_extension, '.jpeg'])
        Image.fromarray(image_np).save(output_image)
        print('\n\nImage saved\n\n')
