


class FaceAPIError(Exception):
    pass

def detect_faces(content: bytes):
    """Detects faces in an image."""
    vertices = [{
                "x": 1112,
                "y": 407
              },
              {
                "x": 1946,
                "y": 407
              },
              {
                "x": 1946,
                "y": 1270
              },
              {
                "x": 1112,
                "y": 1270
              }]
    return [tuple(
        (vertex.x, vertex.y)
         for vertex in vertices
    )]
    # tuple(), tuple((1946, 407)), tuple((1946, 1270)), tuple((1112, 1270))
    # return [tuple(
    #     (vertex.x, vertex.y)
    #               for vertex in face.bounding_poly.vertices)
    #         for face in response.face_annotations]



if __name__ == '__main__':
    from avdc.utility.image import getRawImageByURL

    print(detect_faces(getRawImageByURL('https://www.javbus.com/imgs/cover/1hk2_b.jpg')))
