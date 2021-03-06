import os
import argparse
from pathlib import Path
import random
import shutil

def get_args():
    parser = argparse.ArgumentParser("Dataset Creator for DeepFake Detection Task")
    parser.add_argument(
        "-c",
        "--path-challenge",
        type=str,
        help="Absolute path the root directory of the single sets (challenge dataset).",
    )
    parser.add_argument(
        "-f",
        "--path-ff",
        type=str,
        help="Absolute path the root directory of the single sets (ff dataset).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Name the output directory",
    )
    parser.add_argument(
        "-sv",
        "--split_val",
        default="20",
        type=str,
        help="Percentage of validation set split wrt training set",
    )
    parser.add_argument(
        "-st",
        "--split_test",
        default="20",
        type=str,
        help="Percentage of test set split wrt complete set",
    )
    args = parser.parse_args()
    return args


def main(opt):
    output_dir = opt.output
    main_path_challenge = Path(opt.path_challenge)
    main_path_ff = Path(opt.path_ff)

    
    imgs = sorted(sorted(main_path_challenge.rglob('*.png')) + sorted(main_path_challenge.rglob('*.jpg')) + sorted(main_path_ff.rglob('*.jpg')) + sorted(main_path_ff.rglob('*.png')))
    random.shuffle(imgs)
    i = 0
    v = 0
    for im in imgs:
        if str(main_path_ff) in str(im):
            i += 1
        elif str(main_path_challenge) in str(im):
            v += 1
    print(f'{i} immagini ff, {v} immagini challenge')
    
    print('There are ' + str(len(imgs)) + ' images.\n')
    trainval_len = len(imgs) * (100 - int(opt.split_test)) // 100
    val_len = trainval_len * (int(opt.split_val)) // 100
    test_len = len(imgs) - trainval_len
    train_len = trainval_len - val_len
    print('Training set: ' + str(train_len) + ' images.')
    print('Validation set: ' + str(val_len) + ' images.')
    print('Test set: ' + str(test_len) + ' images.\n')
    print('STARTING DATASET CREATION...')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    test_dir = os.path.join(output_dir, 'test')
    train_dir = os.path.join(output_dir, 'train')
    val_dir = os.path.join(output_dir, 'validation')

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)    
    
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)

    if not os.path.exists(val_dir):
        os.makedirs(val_dir)
    
    c = 0
    image_id = 0

    count_real = 0
    count_fake = 0

    #creation of test_set
    for im in imgs[0:test_len]:
        c += 1
        shutil.copyfile(im, os.path.join(test_dir, str(image_id)+im.suffix))
        label_filename = str(image_id)+'.txt'
        with open(os.path.join(test_dir, label_filename), 'w') as f:
            if str(main_path_challenge) in str(im):        
                f.write(im.parent.stem[0])
                if im.parent.stem[0] == '0':
                    count_real += 1
                else:
                    count_fake += 1
            elif str(main_path_ff) in str(im):
                if "original" in str(im.stem):
                    f.write('0')
                    count_real += 1
                elif "manipulated" in str(im.stem):
                    f.write('1')
                    count_fake += 1

        if c%1000 == 0:
            print(str(c)+' elements processed.')
        image_id += 1


    image_id = 0
    #creation of training_set
    for im in imgs[test_len:test_len+train_len]:
        c += 1
        shutil.copyfile(im, os.path.join(train_dir, str(image_id)+im.suffix))
        label_filename = str(image_id)+'.txt'
        with open(os.path.join(train_dir, label_filename), 'w') as f:
            if str(main_path_challenge) in str(im):        
                f.write(im.parent.stem[0])
                if im.parent.stem[0] == '0':
                    count_real += 1
                else:
                    count_fake += 1
            elif str(main_path_ff) in str(im):
                if "original" in str(im.stem):
                    f.write('0')
                    count_real += 1
                elif "manipulated" in str(im.stem):
                    f.write('1')
                    count_fake += 1
        
        if c%1000 == 0:
            print(str(c)+' elements processed.')
        image_id += 1

    image_id = 0
    #creation of val_set
    for im in imgs[test_len+train_len:test_len+train_len+val_len]:
        c += 1
        shutil.copyfile(im, os.path.join(val_dir, str(image_id)+im.suffix))
        label_filename = str(image_id)+'.txt'
        with open(os.path.join(val_dir, label_filename), 'w') as f:
            if str(main_path_challenge) in str(im):        
                f.write(im.parent.stem[0])
                if im.parent.stem[0] == '0':
                    count_real += 1
                else:
                    count_fake += 1
            elif str(main_path_ff) in str(im):
                if "original" in str(im.stem):
                    f.write('0')
                    count_real += 1
                elif "manipulated" in str(im.stem):
                    f.write('1')
                    count_fake += 1

        if c%1000 == 0:
            print(str(c)+' elements processed.')
        image_id += 1
    
    print('Real images: ' + str(count_real))
    print('Fake images: ' + str(count_fake))

    print('FINISHED!')

    # elif d_type == 'ff':
        
    #     imgs = sorted(sorted(main_path_ff.rglob('*.png')) + sorted(main_path_ff.rglob('*.jpg')))
    #     random.shuffle(imgs)
        
    #     print('There are ' + str(len(imgs)) + ' images.\n')
    #     trainval_len = len(imgs) * (100 - int(opt.split_test)) // 100
    #     val_len = trainval_len * (int(opt.split_val)) // 100
    #     test_len = len(imgs) - trainval_len
    #     train_len = trainval_len - val_len
    #     print('Training set: ' + str(train_len) + ' images.')
    #     print('Validation set: ' + str(val_len) + ' images.')
    #     print('Test set: ' + str(test_len) + ' images.\n')
    #     print('STARTING DATASET CREATION...')

    #     if not os.path.exists(output_dir):
    #         os.makedirs(output_dir)

        
    #     test_dir = os.path.join(output_dir, 'test')
    #     train_dir = os.path.join(output_dir, 'train')
    #     val_dir = os.path.join(output_dir, 'validation')

    #     if not os.path.exists(test_dir):
    #         os.makedirs(test_dir)    
        
    #     if not os.path.exists(train_dir):
    #         os.makedirs(train_dir)

    #     if not os.path.exists(val_dir):
    #         os.makedirs(val_dir)
        
    #     c = 0
    #     image_id = 0

    #     count_real = 0
    #     count_fake = 0

    #     #creation of test_set
    #     for im in imgs[0:test_len]:
    #         c += 1
    #         shutil.copyfile(im, os.path.join(test_dir, str(image_id)+im.suffix))
    #         label_filename = str(image_id)+'.txt'
    #         with open(os.path.join(test_dir, label_filename), 'w') as f:
    #             if "original" in str(im):
    #                 f.write('0')
    #                 count_real += 1
    #             elif "manipulated" in str(im):
    #                 f.write('1')
    #                 count_fake += 1

    #         if c%1000 == 0:
    #             print(str(c)+' elements processed.')
    #         image_id += 1


    #     image_id = 0
    #     #creation of training_set
    #     for im in imgs[test_len:test_len+train_len]:
    #         c += 1
    #         shutil.copyfile(im, os.path.join(train_dir, str(image_id)+im.suffix))
    #         label_filename = str(image_id)+'.txt'
    #         with open(os.path.join(test_dir, label_filename), 'w') as f:
    #             if "original" in str(im):
    #                 f.write('0')
    #                 count_real += 1
    #             elif "manipulated" in str(im):
    #                 f.write('1')
    #                 count_fake += 1
            
    #         if c%1000 == 0:
    #             print(str(c)+' elements processed.')
    #         image_id += 1

    #     image_id = 0
    #     #creation of val_set
    #     for im in imgs[test_len+train_len:test_len+train_len+val_len]:
    #         c += 1
    #         shutil.copyfile(im, os.path.join(val_dir, str(image_id)+im.suffix))
    #         label_filename = str(image_id)+'.txt'
    #         with open(os.path.join(test_dir, label_filename), 'w') as f:
    #             if "original" in str(im):
    #                 f.write('0')
    #                 count_real += 1
    #             elif "manipulated" in str(im):
    #                 f.write('1')
    #                 count_fake += 1
                
    #         if c%1000 == 0:
    #             print(str(c)+' elements processed.')
    #         image_id += 1
        
    #     print('Real images: ' + str(count_real))
    #     print('Fake images: ' + str(count_fake))

    #     print('FINISHED!')


if __name__ == "__main__":
    options = get_args()
    main(options)