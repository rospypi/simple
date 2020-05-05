#pragma once

// for winerror.h
#ifdef NO_ERROR
#undef NO_ERROR
#endif

namespace tf2_msgs {

struct TF2Error {
  enum {
    NO_ERROR = 0u,
    LOOKUP_ERROR = 1u,
    CONNECTIVITY_ERROR = 2u,
    EXTRAPOLATION_ERROR = 3u,
    INVALID_ARGUMENT_ERROR = 4u,
    TIMEOUT_ERROR = 5u,
    TRANSFORM_ERROR = 6u,
  };
};

}
