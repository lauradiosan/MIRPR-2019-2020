

class Backbone_Freezer():
    """
    Handles the freezing/unfreezing of the backbone of the model dynamically during training
    works for MobileNetV2
    """
    def __init__(self, params, freeze_idx=19):
        self.params = params
        self.freeze_idx = freeze_idx

    def freeze_backbone(self, model):
        for params in model.backbone.parameters():
            params.requires_grad = False

    def unfreeze_from(self, layer_idx, model):
        """
        MobileNetV2 has 19 residual bottleneck layers
        unfreezes layers from layer_idx to 18
        """
        for i in range(layer_idx, 19):
            for parameters in model.backbone.features[i].parameters():
                parameters.requires_grad = True

    def step(self, epoch, model):
        """
        from epochs 3 to 7, unfreeze 3 layers at each epoch
        if backbone was not frozen, this has no effect
        """
        if 3 <= epoch and epoch <= 7:
            freeze_idx = self.freeze_idx - (epoch - 2) * 3
            self.unfreeze_from(freeze_idx, model)

        # when the second decay is reached, unfreeze the final layers as well
        if epoch == self.params.second_decay:
            self.unfreeze_from(0, model)
