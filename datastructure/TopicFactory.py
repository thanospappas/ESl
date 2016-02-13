from datastructure.TopTopic import TopTopic
from datastructure.ControvertialTopic import ControvertialTopic


class TopicFactory:

  # Create based on class name:
    def factory(self, type):
        if type == "top": return TopTopic()
        if type == "controvertial": return ControvertialTopic()
        assert 0, "Bad type: " + type