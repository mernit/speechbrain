#!/usr/bin/python
import os
import speechbrain as sb
from complex_ctc_brain import CTCBrain

experiment_dir = os.path.dirname(os.path.realpath(__file__))
hyperparams_file = os.path.join(experiment_dir, "hyperparams.yaml")
data_folder = "../../../../samples/audio_samples/nn_training_samples"
data_folder = os.path.realpath(os.path.join(experiment_dir, data_folder))
with open(hyperparams_file) as fin:
    hyperparams = sb.yaml.load_extended_yaml(fin, {"data_folder": data_folder})

train_set = hyperparams.train_loader()
first_x, first_y = next(iter(train_set))
ctc_brain = CTCBrain(
    modules=hyperparams.modules,
    optimizers={"model": hyperparams.optimizer},
    device="cpu",
    first_inputs=[first_x],
)
ctc_brain.fit(
    range(hyperparams.N_epochs), train_set, hyperparams.valid_loader()
)
test_stats = ctc_brain.evaluate(hyperparams.test_loader())


# Integration test: check that the model overfits the training data
def test_error():
    assert ctc_brain.train_loss < 0.8
