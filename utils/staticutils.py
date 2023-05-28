def saveImage(image):
    image.save(r'./static/img/' + image.filename)
    return '/static/img/'+image.filename