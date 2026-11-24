#include <memory>
#include "rclcpp/rclcpp.hpp"

int main (int argc, char * argv) {

    //initialise ROS2
    rclcpp::init(argc, argv);

    //Create the node with the name Odom_monitor
    auto node = std::make_shared<rclcpp::Node>("Odom_monitor");

    //writing information message to the terminal 
    RCLCPP_INFO(node->get_logger(), "Mini Tesla's Motor is running!");

    //Process the callbacks and wait for the work interupt
    rclcpp::spin(node);

    //Shutdown the process
    rclcpp::shutdown();

    return 0;

}