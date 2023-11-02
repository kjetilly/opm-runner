class Submitter:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Use a subclass of Submitter")
    
    def waitall(self):
        raise NotImplementedError("Use a subclass of Submitter")