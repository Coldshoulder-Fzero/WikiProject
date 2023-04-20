document.addEventListener("DOMContentLoader", change_image)

const image_Dict = [
    
]
  def change_image(self, index):
        current = 1
        image_list = ["https://storage.googleapis.com/thewikicontent/atari.jpg", "https://storage.googleapis.com/thewikicontent/cookieClicker.jpg", "https://storage.googleapis.com/thewikicontent/DS.jpg","https://storage.googleapis.com/thewikicontent/mobilegaming.png","https://storage.googleapis.com/thewikicontent/nintendo.jfif", "https://storage.googleapis.com/thewikicontent/playStation.jpg", "https://storage.googleapis.com/thewikicontent/sega.jpg", "https://storage.googleapis.com/thewikicontent/steam.png", "https://storage.googleapis.com/thewikicontent/tetris.png", "https://storage.googleapis.com/thewikicontent/wii.jpg", "https://storage.googleapis.com/thewikicontent/Xbox.jpg" ]    
        
        imageURL = image_list(current+index)

        return render_template('main.html', imageUrl = imageUrl)  