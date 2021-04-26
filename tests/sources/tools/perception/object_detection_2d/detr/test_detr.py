# Copyright 2020-2021 OpenDR European Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import unittest
import shutil
import os
import torch
from perception.object_detection_2d.detr.detr_learner import DetrLearner

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

print("Using device:", DEVICE)
print("Using device:", DEVICE, file=sys.stderr)


def rmfile(path):
    try:
        os.remove(path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def rmdir(_dir):
    try:
        shutil.rmtree(_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


class TestDetrLearner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = os.path.join("tests", "sources", "tools",
                                    "perception", "object_detection_2d",
                                    "detr",
                                    "detr_temp")

        cls.model_backbones = "resnet50"

        # TODO: Get dataset from server
        cls.dataset_path = "/home/jelle/nano"

        print("Dataset downloaded", file=sys.stderr)

        learner = DetrLearner(temp_path=cls.temp_dir)

        learner.download(backbone=model_backbone)

        print("Model downloaded", file=sys.stderr)

    @classmethod
    def tearDownClass(cls):
        # Clean up downloaded files

        rmdir(os.path.join(cls.temp_dir))

    def test_fit(self):

        def test_model(name):
            dataset = MotDat(self.dataset_path)

            learner = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )

            starting_param = list(learner.model.parameters())[0].clone()

            learner.fit(
                dataset,
                val_epochs=-1,
                train_split_paths=self.train_split_paths,
                val_split_paths=self.train_split_paths,
                verbose=True,
            )
            new_param = list(learner.model.parameters())[0].clone()
            self.assertFalse(torch.equal(starting_param, new_param))

            print("Fit", name, "ok", file=sys.stderr)

        for name in self.model_names:
            test_model(name)

    def test_fit_iterator(self):
        def test_model(name):
            dataset = MotDatasetIterator(self.dataset_path, self.train_split_paths)
            eval_dataset = RawMotDatasetIterator(self.dataset_path, self.train_split_paths)

            learner = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )

            starting_param = list(learner.model.parameters())[0].clone()

            learner.fit(
                dataset,
                val_dataset=eval_dataset,
                val_epochs=-1,
                train_split_paths=self.train_split_paths,
                val_split_paths=self.train_split_paths,
                verbose=True,
            )
            new_param = list(learner.model.parameters())[0].clone()
            self.assertFalse(torch.equal(starting_param, new_param))

            print("Fit iterator", name, "ok", file=sys.stderr)

        for name in self.model_names:
            test_model(name)

    def test_eval(self):
        def test_model(name):
            model_path = os.path.join(self.temp_dir, name)
            eval_dataset = RawMotDatasetIterator(self.dataset_path, self.train_split_paths)

            learner = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )
            learner.load(model_path, verbose=True)
            result = learner.eval(eval_dataset)

            self.assertGreater(len(result["mota"]), 0)

        for name in self.model_names:
            test_model(name)

    def test_infer(self):
        def test_model(name):
            model_path = os.path.join(self.temp_dir, name)
            eval_dataset = RawMotDatasetIterator(self.dataset_path, self.train_split_paths)

            learner = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )
            learner.load(model_path, verbose=True)
            result = learner.infer(eval_dataset[0][0], 10)

            self.assertTrue(len(result) > 0)

            result = learner.infer([
                eval_dataset[0][0],
                eval_dataset[1][0],
            ])

            self.assertTrue(len(result) == 2)
            self.assertTrue(len(result[0]) > 0)

        for name in self.model_names:
            test_model(name)

    def test_save(self):
        def test_model(name):
            model_path = os.path.join(self.temp_dir, "test_save_" + name)
            save_path = os.path.join(model_path, "save")

            learner = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )

            learner.save(save_path, True)
            starting_param_1 = list(learner.model.parameters())[0].clone()

            learner2 = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )
            learner2.load(save_path)

            new_param = list(learner2.model.parameters())[0].clone()
            self.assertTrue(torch.equal(starting_param_1, new_param))

        for name in self.model_names:
            test_model(name)

    def test_optimize(self):
        def test_model(name):

            learner = ObjectTracking2DFairMotLearner(
                iters=1,
                num_epochs=1,
                checkpoint_after_iter=3,
                temp_path=self.temp_dir,
                device=DEVICE,
            )

            with self.assertRaises(Exception):
                learner.optimize()

        for name in self.model_names:
            test_model(name)


if __name__ == "__main__":
    unittest.main()
