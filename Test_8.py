joy = {"short_id": "dCbmQw8s", "countries": ["us"], "square_image": {"uri": "vibbidi-images/albums/img_7DBA818CB9CA4117891E22262A4A5CBB.2020.11.26.14.15.40.jpg", "width": 1000, "height": 1000, "mime_type": "image/jpeg", "resize_images": []}}
k = joy.get("square_image", {}).get("uri")
print(k)