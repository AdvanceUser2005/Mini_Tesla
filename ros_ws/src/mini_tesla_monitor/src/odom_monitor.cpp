#include <memory>
#include "rclcpp/rclcpp.hpp"

int main(int argc, char * argv) {
     rclcpp::init(argc, argv);
     auto node = std::make_shared<rclcpp::Node>("odom_monitor");
     RCLCPP_INFO(node->get_logger(), "Mini Tesla Motor is running!");
     rclcpp::spin(node);
     rclcpp::shutdown();
     return 0;
}