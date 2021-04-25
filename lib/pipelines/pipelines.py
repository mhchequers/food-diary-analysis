class GenericPipeline:
    def __init__(self, df, pipeline_components: list):
        self.df = df
        self.pipeline_components = pipeline_components

    def run(self):
        print("Starting to run pipeline...")

        for pipeline_component in self.pipeline_components:
            component = pipeline_component[0]
            options = pipeline_component[1]
            self.df = component(self.df, options).run()

        print("Finished running pipeline...")

        return self.df
