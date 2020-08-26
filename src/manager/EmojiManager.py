class EmojiManager():

  def __init__(self):
    self.emojiIdDict = {}
  
  '''
  emojiName : str
  emojiId   : int
  '''
  def registerEmoji(self, emojiName, emojiId):
    self.emojiIdDict[emojiName] = emojiId
  
  def getEmojiDict(self):
    return self.emojiIdDict