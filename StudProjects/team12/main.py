from torch.utils.tensorboard import SummaryWriter
from train.loss_fn import Detection_Loss
import torch
import torch.optim as optim

from train.config import Params
from general_config import anchor_config
from train.helpers import *
from train import train
from train.validate import Model_evaluator
from train.optimizer_handler import *
from data import dataloaders
from architectures.models import SSDNet
from misc import cross_validation


def run(path='misc/experiments/ssdnet/params.json', resume=False, eval_only=False, cross_validate=False):
    '''
    args: path - string path to the json config file
    trains model refered by that file, saves model and optimizer dict at the same location
    '''
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    params = Params(path)

    print("MODEL ID: ", params.model_id)
    if params.model_id == 'ssdnet':
        print("List of anchors per feature map cell: ", anchor_config.k_list)
        model = SSDNet.SSD_Head(n_classes=params.n_classes, k_list=anchor_config.k_list)
    model.to(device)

    if params.optimizer == 'adam':
        optimizer = layer_specific_adam(model, params)
    elif params.optimizer == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=params.learning_rate,
                              weight_decay=params.weight_decay, momentum=0.9)

    print('Number of epochs:', params.n_epochs)
    print('Total number of parameters of model: ',
          sum(p.numel() for p in model.parameters()))
    print('Total number of trainable parameters of model: ',
          sum(p.numel() for p in model.parameters() if p.requires_grad))

    start_epoch = 0
    if resume or eval_only or cross_validate:
        checkpoint = torch.load('misc/experiments/{}/model_checkpoint'.format(params.model_id))
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch']
        print('Model loaded successfully')

    print('Total number of parameters given to optimizer: ')
    print(sum(p.numel() for pg in optimizer.param_groups for p in pg['params']))
    print('Total number of trainable parameters given to optimizer: ')
    print(sum(p.numel() for pg in optimizer.param_groups for p in pg['params'] if p.requires_grad))

    train_loader, valid_loader = dataloaders.get_dataloaders(params)

    print('Train size: ', len(train_loader), len(
        train_loader.dataset), len(train_loader.sampler.sampler))
    print('Val size: ', len(valid_loader), len(
        valid_loader.dataset), len(valid_loader.sampler.sampler))

    writer = SummaryWriter(filename_suffix=params.model_id)
    anchors, grid_sizes = create_anchors()
    anchors, grid_sizes = anchors.to(device), grid_sizes.to(device)

    detection_loss = Detection_Loss(anchors, grid_sizes, device, params)
    model_evaluator = Model_evaluator(valid_loader, detection_loss, writer=writer, params=params)

    if eval_only:
        model_evaluator.complete_evaluate(model, optimizer, train_loader)

    elif cross_validate:
        cross_validation.cross_validate(
            model, detection_loss, valid_loader, model_evaluator, params)

    else:
        train.train(model, optimizer, train_loader, model_evaluator,
                    detection_loss, params, start_epoch)

# run()
