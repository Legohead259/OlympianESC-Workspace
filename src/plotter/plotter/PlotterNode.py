#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import matplotlib.pyplot as plt
from motor_interfaces.msg import AngularMeasurement

class PlotterNode(Node):
    def __init__(self):
        super().__init__('plotter_node')
        self.subscription = self.create_subscription(
            AngularMeasurement,
            'angular_position',  # Replace with the actual topic name
            self.callback,
            10)
        self.timestamps = []
        self.positions = []
        self.velocities = []
        self.max_data_points = 50  # Set the maximum number of data points to display

        # Set up subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, sharex=True)

    def callback(self, msg):
        self.timestamps.append(msg.timestamp)
        self.positions.append(msg.angular_position)
        self.velocities.append(msg.angular_velocity)

        # Cap the size of the arrays at max_data_points
        if len(self.timestamps) > self.max_data_points:
            self.timestamps.pop(0)
            self.positions.pop(0)
            self.velocities.pop(0)

        self.plot()

    def plot(self):
        # Plot angular positions
        self.ax1.clear()
        self.ax1.plot(self.timestamps, self.positions, label='Angular Position')
        self.ax1.set_ylabel('Position (rad)')
        self.ax1.legend()

        # Plot angular velocities
        self.ax2.clear()
        self.ax2.plot(self.timestamps, self.velocities, label='Angular Velocity')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Velocity (rad/s)')
        self.ax2.legend()

        # Show the plot
        plt.pause(0.01)
        plt.draw()

def main(args=None):
    rclpy.init(args=args)
    node = PlotterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
