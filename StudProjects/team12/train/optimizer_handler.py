import torch
import torch.optim as optim

def layer_specific_adam(model, params):
    return optim.Adam([
                {'params': model.backbone.parameters(), 'lr':params.learning_rate * params.decay_rate},
                {'params': model.out1.parameters()},
                {'params': model.out2.parameters()},
                {'params': model.inv2.parameters()},
                {'params': model.out3.parameters()},
                {'params': model.inv3.parameters()},
                {'params': model.out4.parameters()},
                {'params': model.inv4.parameters()},
                {'params': model.out5.parameters()},
                {'params': model.inv5.parameters()},
            ], lr=params.learning_rate, weight_decay=params.weight_decay)

def plain_adam(model, params):
    return optim.Adam(model.parameters(), lr=params.learning_rate, weight_decay=params.weight_decay)
