import os
import json
import subprocess
import numpy as np
import pandas as pd

def flatten_vrd_relationship(img, relationship, objects, predicates):
    """Create a per-relationship entry from a per-image entry JSON."""
    new_relationship_dict = {}
    
    new_relationship_dict["subject_category"] = objects[relationship["subject"]["category"]]
    new_relationship_dict["object_category"] = objects[relationship["object"]["category"]]
    
    new_relationship_dict["subject_bbox"] = relationship["subject"]["bbox"]
    new_relationship_dict["object_bbox"] = relationship["object"]["bbox"]

    new_relationship_dict["label"] = relationship["predicate"]
    new_relationship_dict["sent"] = objects[relationship["subject"]["category"]] + " " + predicates[relationship["predicate"]] + " " + objects[relationship["object"]["category"]]
    
    new_relationship_dict["source_img"] = img

    return new_relationship_dict

def vrd_to_pandas(relationships_set, objects, predicates):
    """Create Pandas DataFrame from JSON of relationships."""
    relationships = []

    for img in relationships_set:
      img_relationships = relationships_set[img]
      for relationship in img_relationships:
        relationships.append(flatten_vrd_relationship(img, relationship, objects, predicates))
    return pd.DataFrame.from_dict(relationships)

def load_vrd_data():
  relationships_train = json.load(open("/content/drive/My Drive/visual_relation/json_dataset/annotations_train.json"))
  relationships_test = json.load(open("/content/drive/My Drive/visual_relation/json_dataset/annotations_test.json"))
  objects = json.load(open("/content/drive/My Drive/visual_relation/json_dataset/objects.json"))
  predicates = json.load(open("/content/drive/My Drive/visual_relation/json_dataset/predicates.json"))

  np.random.seed(123)
  val_idx = list(np.random.choice(len(relationships_train), 1000, replace=False))
  relationships_val = {
    key: value
    for i, (key, value) in enumerate(relationships_train.items())
    if i in val_idx
  }
  relationships_train = {
    key: value
    for i, (key, value) in enumerate(relationships_train.items())
    if i not in val_idx
  }
  train_df = vrd_to_pandas(relationships_train,objects,predicates)
  valid_df = vrd_to_pandas(relationships_val,objects,predicates)
  test_df = vrd_to_pandas(relationships_test,objects,predicates)
  return train_df,valid_df,test_df
