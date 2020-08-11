from MLProto.MLProto.Proto import Proto
import data_pull as dp
import argparse

import json
import itertools

def train():

    # load training config values
    with open('model_train_config.json', 'r') as config:
        hypers = json.load(config)

    # get list of configs
    keys, values = zip(*my_dict.items())
    config_dict = [dict(zip(keys, v)) for v in itertools.product(*values)]

    # get data
    data = dp.cloud_to_df()
    print(data)
    print()

    # buffer for comparison metrics
    metrics = {}

    # iterate through configurations
    iteration = 0
    for config in config_dict:

        # create model with given config
        model = Proto('model'+str(iteration), data, 2, depth=config['depth'], node_counts=config['node_counts'][:config['depth']], \
                    batch=config['batch'], test_size=config['test_size'], loss=config['loss'], learning_rate=config['learning_rate'], past_window=config['past_window'])

        # write summary for each model to log file
        print(model.identifier + '\n----------------------------------------')
        print(model.model.summary())
        print('TRAINING\n')

        # train model for 10 epochs
        model.train(10, True, True)

        # evaluate and record loss
        print('EVALUATING\n')
        model.evaluate()
        metrics[model.loss] = model.identifier

        # save model to models directory
        print('SAVING\n')
        model.save_model()

        print('FINISHED ' + model.identifier)

    print('BEST MODEL: ' + metrics[min(metrics.keys())] + '\n')

if __name__ == '__main__':
    train()