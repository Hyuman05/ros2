import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():

    translator = launch_ros.actions.Node(
        package='mypkg',
        executable='translator',
        name='translator',
        output='screen',
        )
    questioner = launch_ros.actions.Node(
        package='mypkg',
        executable='questioner',
        name='questioner',
        output='screen',
        )

    return launch.LaunchDescription([translator, questioner])
