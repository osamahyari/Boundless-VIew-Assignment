import json
file_path = "instances_train.json"
with open(file_path, "r") as f:
    json_data = json.load(f)
images = json_data["images"]
# annotations = json_data["annotations"]
#image_ids = {img["id"] for img in images}
image_file_name = {img["file_name"] for img in images}
print(len(image_file_name))

# annotation_img_ids = {ann["image_id"] for ann in annotations}
# orphan_images = [img_id for img_id in image_ids if img_id not in annotation_img_ids]
# orphan_ann_img_ids = [ann_img_id for ann_img_id in annotation_img_ids if ann_img_id not in image_ids]
#
# print("orphan_images", orphan_images)
# print("orphan_ann_img_ids", orphan_ann_img_ids)
# img_annotations = {
#     img_id: []
#     for img_id in image_ids
# }
# for ann in annotations:
#     img_annotations[ann["image_id"]].append(ann["id"])
# import pprint
# pprint.pprint(img_annotations)