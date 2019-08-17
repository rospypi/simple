#pragma once

#include <string>

#include <ros/time.h>

namespace std_msgs {

struct Header {
  uint32_t seq;
  ros::Time stamp;
  std::string frame_id;
};

};

namespace geometry_msgs {

struct Vector3 {
  double x;
  double y;
  double z;
};

struct Quaternion {
  double x;
  double y;
  double z;
  double w;
};

struct Transform {
  Vector3 translation;
  Quaternion rotation;
};

struct TransformStamped {
  std_msgs::Header header;
  std::string child_frame_id;
  Transform transform;
};

}
