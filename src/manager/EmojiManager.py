class EmojiManager():

  def __init__(self):
    self.emojiIdDict = {}
  
  '''
  emojiName : str class
  emojiId   : Emoji class
  '''
  def registerEmoji(self, emojiList):
    for emoji in emojiList:
      if emoji.name == 'werewolf':
        self.emojiIdDict[emoji.name] = emoji
      if emoji.name == 'knight':
        self.emojiIdDict[emoji.name] = emoji
      if emoji.name == 'fortuneteller':
        self.emojiIdDict[emoji.name] = emoji
  
  def getEmojiDict(self):
    return self.emojiIdDict