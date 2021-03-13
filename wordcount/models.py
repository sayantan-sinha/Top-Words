from django.db import models
import json

# Create your models here.
class WordTree(models.Model):
    link = models.TextField()
    words = models.TextField()

    def __str__(self):
        return self.link

    def store_strings(self, words):
        word_s = json.dumps(words)
        self.words = word_s
        self.save()

    def get_strings(self):
        json_dec = json.decoder.JSONDecoder()
        word_l = json_dec.decode(self.words)
        return word_l