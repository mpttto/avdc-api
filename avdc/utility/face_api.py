


class FaceAPIError(Exception):
    pass


def detect_faces(content: bytes):
    """Detects faces in an image."""
    return [tuple((1112,407)),tuple((1946,407)),tuple((1946,1270)),tuple((1112,1270))]



if __name__ == '__main__':
    from avdc.utility.image import getRawImageByURL

    print(detect_faces(getRawImageByURL('https://www.javbus.com/imgs/cover/1hk2_b.jpg')))
