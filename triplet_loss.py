import keras.backend as K

from constants import *

alpha = 0.1


def cosine_proximity(y_true, y_pred):
    y_true = K.l2_normalize(y_true, axis=-1)
    y_pred = K.l2_normalize(y_pred, axis=-1)
    return y_true * y_pred


def deep_speaker_loss(x1, x2):
    # x1.shape = (batch_size, embedding_size)
    # x2.shape = (batch_size, embedding_size)
    # CONVENTION: Input is:
    # concat(BATCH_SIZE * [ANCHOR, POSITIVE_EX, NEGATIVE_EX] * NUM_FRAMES)
    # EXAMPLE:
    # BATCH_NUM_TRIPLETS = 3, NUM_FRAMES = 2
    # _____________________________________________________
    # ANCHOR 1 (512,)
    # ANCHOR 2 (512,)
    # ANCHOR 3 (512,)
    # POS EX 1 (512,)
    # POS EX 2 (512,)
    # POS EX 3 (512,)
    # NEG EX 1 (512,)
    # NEG EX 2 (512,)
    # NEG EX 3 (512,)
    # ANCHOR 1 # FROM HERE (INCLUDED), THIS IS THE SAME BLOCK AS ABOVE.
    # ANCHOR 2 # WE ADD IT BECAUSE WE WANT TO MATCH THE SIZE FOR KERAS.
    # ANCHOR 3 # BATCH_SIZE * NUM_FRAMES => BATCH_SIZE => BATCH_SIZE * NUM_FRAMES
    # POS EX 1 (512,)
    # POS EX 2 (512,)
    # POS EX 3 (512,)
    # NEG EX 1 (512,)
    # NEG EX 2 (512,)
    # NEG EX 3 (512,)
    # _____________________________________________________

    # WE UPSCALE with K.tile() so we have to remove the garbage. It's redundant.

    x1 = x1[0:BATCH_NUM_TRIPLETS * 3]

    anchor = x1[0:BATCH_NUM_TRIPLETS]
    positive_ex = x1[BATCH_NUM_TRIPLETS:2 * BATCH_NUM_TRIPLETS]
    negative_ex = x1[2 * BATCH_NUM_TRIPLETS:]

    sap = cosine_proximity(anchor, positive_ex)
    san = cosine_proximity(anchor, negative_ex)
    loss = K.mean(K.abs(san - sap + alpha))

    # we multiply x2 by 0 to have its gradient to be 0.
    # if we don't x2, its gradient is equal to None and it raises an error.
    # with our convention, we focus solely on x1 because the targets are given by the structure described above
    # with (anchor, positive examples, negative examples)
    return loss + 0 * x2
