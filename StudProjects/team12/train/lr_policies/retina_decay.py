class Lr_decay:
    '''
    Implements learning rate decay similar to the retina net paper:
    initial learning rate of 0.01, which is then
    divided by 10 at certain steps
    '''

    def __init__(self, lr, start_epoch, params):
        self.lr = lr
        self.current_step = start_epoch
        self.params = params

    def step(self, optimizer):
        self.current_step += 1

        if self.current_step == self.params.first_decay:
            # don't want to decay backbone here as it starts at a lower lr
            for idx, param_gr in enumerate(optimizer.param_groups):
                if idx == 0:
                    continue
                param_gr['lr'] *= self.params.decay_rate

        if self.current_step == self.params.second_decay:
            for param_gr in optimizer.param_groups:
                param_gr['lr'] *= self.params.decay_rate

        if self.current_step == self.params.third_decay:
            for param_gr in optimizer.param_groups:
                param_gr['lr'] *= self.params.decay_rate
