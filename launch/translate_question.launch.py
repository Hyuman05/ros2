import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():

    translator = launch_ros.actions.Node(
        package='mypkg',
        executable='translator'
        )
    questioner = launch_ros.actions.Node(
        package='mypkg',
        executable='questioner',
        output='screen'
        )

    return launch.LaunchDescription([translator, questioner])
