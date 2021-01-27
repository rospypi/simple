import cv2

_CV_TYPES = {
    "rgb8": cv2.CV_8UC3,
    "rgba8": cv2.CV_8UC4,
    "rgb16": cv2.CV_16UC3,
    "rgba16": cv2.CV_16UC4,
    "bgr8": cv2.CV_8UC3,
    "bgra8": cv2.CV_8UC4,
    "bgr16": cv2.CV_16UC3,
    "bgra16": cv2.CV_16UC4,
    "mono8": cv2.CV_8UC1,
    "mono16": cv2.CV_16UC1,
    "bayer_rggb8": cv2.CV_8UC1,
    "bayer_bggr8": cv2.CV_8UC1,
    "bayer_gbrg8": cv2.CV_8UC1,
    "bayer_grbg8": cv2.CV_8UC1,
    "bayer_rggb16": cv2.CV_16UC1,
    "bayer_bggr16": cv2.CV_16UC1,
    "bayer_gbrg16": cv2.CV_16UC1,
    "bayer_grbg16": cv2.CV_16UC1,
    "yuv422": cv2.CV_8UC2,
    }

_CV_CONVERSIONS = {
    ("mono8", "rgb8"): cv2.COLOR_GRAY2RGB,
    ("mono8", "bgr8"): cv2.COLOR_GRAY2BGR,
    ("mono8", "rgba8"): cv2.COLOR_GRAY2RGBA,
    ("mono8", "bgra8"): cv2.COLOR_GRAY2BGRA,

    ("rgb8", "mono8"): cv2.COLOR_RGB2GRAY,
    ("rgb8", "bgr8"): cv2.COLOR_RGB2BGR,
    ("rgb8", "rgba8"): cv2.COLOR_RGB2RGBA,
    ("rgb8", "bgra8"): cv2.COLOR_RGB2BGRA,

    ("bgr8", "mono8"): cv2.COLOR_BGR2GRAY,
    ("bgr8", "rgb8"): cv2.COLOR_BGR2RGB,
    ("bgr8", "rgba8"): cv2.COLOR_BGR2RGBA,
    ("bgr8", "bgra8"): cv2.COLOR_BGR2BGRA,

    ("rgba8", "mono8"): cv2.COLOR_RGBA2GRAY,
    ("rgba8", "rgb8"): cv2.COLOR_RGBA2RGB,
    ("rgba8", "bgr8"): cv2.COLOR_RGBA2BGR,
    ("rgba8", "bgra8"): cv2.COLOR_RGBA2BGRA,

    ("bgra8", "mono8"): cv2.COLOR_BGRA2GRAY,
    ("bgra8", "rgb8"): cv2.COLOR_BGRA2RGB,
    ("bgra8", "bgr8"): cv2.COLOR_BGRA2BGR,
    ("bgra8", "rgba8"): cv2.COLOR_BGRA2RGBA,

    ("yuv422", "mono8"): cv2.COLOR_YUV2GRAY_UYVY,
    ("yuv422", "rgb8"): cv2.COLOR_YUV2RGB_UYVY,
    ("yuv422", "bgr8"): cv2.COLOR_YUV2BGR_UYVY,
    ("yuv422", "rgba8"): cv2.COLOR_YUV2RGBA_UYVY,
    ("yuv422", "bgra8"): cv2.COLOR_YUV2BGRA_UYVY,

    ("bayer_rggb8", "mono8"): cv2.COLOR_BayerBG2GRAY,
    ("bayer_rggb8", "rgb8"): cv2.COLOR_BayerBG2RGB,
    ("bayer_rggb8", "bgr8"): cv2.COLOR_BayerBG2BGR,

    ("bayer_bggr8", "mono8"): cv2.COLOR_BayerRG2GRAY,
    ("bayer_bggr8", "rgb8"): cv2.COLOR_BayerRG2RGB,
    ("bayer_bggr8", "bgr8"): cv2.COLOR_BayerRG2BGR,

    ("bayer_gbrg8", "mono8"): cv2.COLOR_BayerGR2GRAY,
    ("bayer_gbrg8", "rgb8"): cv2.COLOR_BayerGR2RGB,
    ("bayer_gbrg8", "bgr8"): cv2.COLOR_BayerGR2BGR,

    ("bayer_grbg", "mono8"): cv2.COLOR_BayerGB2GRAY,
    ("bayer_grbg", "rgb8"): cv2.COLOR_BayerGB2RGB,
    ("bayer_grbg", "bgr8"): cv2.COLOR_BayerGB2BGR,
    }


def CV_MAKETYPE(depth, cn):
    CV_CN_SHIFT = 3
    CV_DEPTH_MAX = (1 << CV_CN_SHIFT)
    CV_DEPTH_MASK = CV_DEPTH_MAX - 1
    def CV_MAT_DEPTH(flags):
        return ((flags) & CV_DEPTH_MASK)
    return (CV_MAT_DEPTH(depth) + (((cn)-1) << CV_CN_SHIFT))


def depthStrToInt(depth):
    if depth == "8U":
        return 0
    elif depth == "8S":
        return 1
    elif depth == "16U":
        return 2
    elif depth == "16S":
        return 3
    elif depth == "32S":
        return 4
    elif depth == "32F":
        return 5
    else:
        return 6

def getCvType(encoding):
    if encoding in _CV_TYPES:
      return _CV_TYPES[encoding]
    import re
    pre = re.compile("(8U|8S|16U|16S|32S|32F|64F)C([0-9]+)")
    mat = pre.match(encoding)
    if mat:
      return CV_MAKETYPE(depthStrToInt(mat[1]), int(mat[2]))
    pre = re.compile("(8U|8S|16U|16S|32S|32F|64F)")
    mat = pre.match(encoding)
    if mat:
      return CV_MAKETYPE(depthStrToInt(mat[1]), 1)
    raise NotImplemented("Wrong encoding...")


def cvtColorForDisplay():
    raise NotImplementedError("cvtColorForDisplay is not implemented yet")


def CV_MAT_CNWrap(flags):
    return ((((flags) & ((63) << 3)) >> 3) + 1)


def CV_MAT_DEPTHWrap(flags):
    return ((flags) & 7)


def cvtColor2(img, encoding_in, encoding_out):
    if encoding_in == encoding_out:
        return img

    conversion = _CV_CONVERSIONS[(encoding_in, encoding_out)]
    # depth conversion is not yet implemented
    return cv2.cvtColor(img, conversion)
