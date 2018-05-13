"""Collection of hyper parameters, network layout, and reporting options."""

import tensorflow as tf
import numpy as np

from python.s_labels import num_classes


# Constants describing the training process.
tf.flags.DEFINE_string('train_dir', '/home/marc/workspace/speech_checkpoints/ds_lstm_3',
                       """Directory where to write event logs and checkpoints.""")

tf.flags.DEFINE_integer('batch_size', 4,
                        """(Maximum) Number of samples within a batch.""")

# Learning Rate.
tf.flags.DEFINE_float('learning_rate', 1e-3,
                      """Initial learning rate.""")
tf.flags.DEFINE_float('learning_rate_decay_factor', 3/4,
                      """Learning rate decay factor.""")
tf.flags.DEFINE_integer('steps_per_decay', 50000,
                        """Number of epochs after which learning rate decays.""")

# Adam Optimizer.
tf.flags.DEFINE_float('adam_beta1', 0.9,
                      """Adam optimizer beta_1 power.""")
tf.flags.DEFINE_float('adam_beta2', 0.999,
                      """Adam optimizer beta_2 power.""")
tf.flags.DEFINE_float('adam_epsilon', 1e-8,
                      """Adam optimizer epsilon.""")

# CTC loss and decoder.
tf.flags.DEFINE_integer('beam_width', 1024,
                        """Beam width used in the CTC `beam_search_decoder`.""")
tf.flags.DEFINE_bool('use_warp_ctc', False,
                     """Weather to use Baidu's `warp_ctc_loss` or TensorFlow's `ctc_loss`.""")

# Dropout.
tf.flags.DEFINE_float('lstm_dropout_rate', 0.0,
                      """Dropout rate for the RNN cell layers.""")
tf.flags.DEFINE_float('dense_dropout_rate', 0.1,
                      """Dropout rate for dense layers.""")

# Layer and activation options.
tf.flags.DEFINE_integer('num_units_lstm', 2048,
                        """Number of hidden units in each of the BDLSTM cells.""")
tf.flags.DEFINE_integer('num_layers_lstm', 1,
                        """Number of stacked BDLSTM cells.""")
tf.flags.DEFINE_integer('num_units_dense', 2048,
                        """Number of units per dense layer.""")

tf.flags.DEFINE_float('relu_cutoff', 20.0,
                      """Cutoff ReLU activations that exceed the cutoff.""")

# Logging and Output.
# [Deep Speech 1] uses 15 to 20 epochs. 229222samples // 4batch_size * 20epochs = 1146100steps
tf.flags.DEFINE_integer('max_steps', 1000000,
                        """Number of steps/batches to run.""")
tf.flags.DEFINE_integer('log_frequency', 100,
                        """How often (every `log_frequency` steps) to log results.""")
tf.flags.DEFINE_integer('num_samples_to_report', 4,
                        """The maximum number of decoded and original text samples to report.""")

# Dataset.
tf.flags.DEFINE_integer('sampling_rate', 16000,
                        """The sampling rate of the audio files (2 * 8kHz).""")
tf.flags.DEFINE_integer('num_examples_train', 229222,
                        """Number of examples in the training set. `test.txt`""")
tf.flags.DEFINE_integer('num_examples_test', 3775,
                        """Number of examples in the testing/evaluation set. `test.txt`""")
tf.flags.DEFINE_integer('num_examples_validate', 3210,
                        """Number of examples in the validation set. `validate.txt`""")
tf.flags.DEFINE_integer('num_classes', num_classes(),
                        """Number of classes. Contains the additional CTC <blank> label.""")

# Evaluation.
tf.flags.DEFINE_string('eval_dir', '',
                       """If set, evaluation log data will be stored here, instead of the default
                       directory `f'{FLAGS.train_dir}_eval'.""")

# Miscellaneous.
tf.flags.DEFINE_bool('delete', False,
                     """Whether to delete old checkpoints, or resume training.""")
tf.flags.DEFINE_integer('random_seed', 1337,
                        """TensorFlow random seed.""")
tf.flags.DEFINE_boolean('log_device_placement', False,
                        """Whether to log device placement.""")
tf.flags.DEFINE_boolean('allow_vram_growth', True,
                        """Allow TensorFlow to allocate VRAM as needed, 
                        as opposed to allocating the whole VRAM at program start.""")


# Export names.
TF_FLOAT = tf.float32   # ctc_*** functions don't support float64. See #13
NP_FLOAT = np.float32   # ctc_*** functions don't support float64. See #13

FLAGS = tf.flags.FLAGS


def get_parameters():
    """Generate a string containing the training, and network parameters.

    Returns:
        (str): Training parameters.
    """
    s = 'Learning Rage (lr={}, steps_per_decay={}, decay_factor={}); use_warp_ctc={}; ' \
        'BDLSTM (num_units={}, num_layers={}); ' \
        'Dense (num_units={}); ' \
        'Training (batch_size={}, max_steps={}, log_frequency={})'
    return s.format(FLAGS.learning_rate, FLAGS.steps_per_decay,
                    FLAGS.learning_rate_decay_factor, FLAGS.use_warp_ctc,
                    FLAGS.num_units_lstm, FLAGS.num_layers_lstm,
                    FLAGS.num_units_dense,
                    FLAGS.batch_size, FLAGS.max_steps, FLAGS.log_frequency)
