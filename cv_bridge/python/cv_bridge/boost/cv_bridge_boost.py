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
    "8UC1": cv2.CV_8UC1,
    "8UC2": cv2.CV_8UC2,
    "8UC3": cv2.CV_8UC3,
    "8UC4": cv2.CV_8UC4,
    "8SC1": cv2.CV_8SC1,
    "8SC2": cv2.CV_8SC2,
    "8SC3": cv2.CV_8SC3,
    "8SC4": cv2.CV_8SC4,
    "16UC1": cv2.CV_8UC1,
    "16UC2": cv2.CV_8UC2,
    "16UC3": cv2.CV_8UC3,
    "16UC4": cv2.CV_8UC4,
    "16SC1": cv2.CV_16SC1,
    "16SC2": cv2.CV_16SC2,
    "16SC3": cv2.CV_16SC3,
    "16SC4": cv2.CV_16SC4,
    "32SC1": cv2.CV_32SC1,
    "32SC2": cv2.CV_32SC2,
    "32SC3": cv2.CV_32SC3,
    "32SC4": cv2.CV_32SC4,
    "32FC1": cv2.CV_32FC1,
    "32FC2": cv2.CV_32FC2,
    "32FC3": cv2.CV_32FC3,
    "32FC4": cv2.CV_32FC4,
    "64FC1": cv2.CV_64FC1,
    "64FC2": cv2.CV_64FC2,
    "64FC3": cv2.CV_64FC3,
    "64FC4": cv2.CV_64FC4,
    "bayer_rggb8": cv2.CV_8UC1,
    "bayer_bggr8": cv2.CV_8UC1,
    "bayer_gbrg8": cv2.CV_8UC1,
    "bayer_grbg8": cv2.CV_8UC1,
    "bayer_rggb16": cv2.CV_16UC1,
    "bayer_bggr16": cv2.CV_16UC1,
    "bayer_gbrg16": cv2.CV_16UC1,
    "bayer_grbg16": cv2.CV_16UC1,
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


def getCvType(encoding):
    return _CV_TYPES[encoding]


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
