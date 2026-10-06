cmake_minimum_required(VERSION 3.8)
project(mini_tesla_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf meshes launch config worlds
  DESTINATION share/${PROJECT_NAME})

install(PROGRAMS scripts/tof_to_range.py
  DESTINATION lib/${PROJECT_NAME})

ament_package()
