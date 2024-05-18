#!/bin/bash

echo "
-------------------------------------------------
                mobiq_song

** NOTICE **  script_dir can be modified to yours

-------------------------------------------------
                Li Xingyou
-------------------------------------------------
"

# 查找包含特定文件名的所有路径
find_all_target_files() {
    local target_file=$1
    local search_dir=$2
    find "$search_dir" -type f -name "$target_file" | sort
}

# 获取当前脚本的目录路径
script_dir=$(dirname "$(readlink -f "$0")")
echo "script is $script_dir"

target_file="execute_docker.sh"

# 查找所有名为 execute_docker.sh 的文件
all_files=$(find_all_target_files "$target_file" "$script_dir")

# 将所有找到的文件路径存储到数组中
IFS=$'\n' read -rd '' -a files_array <<<"$all_files"

# 处理找到的所有文件
if [ ${#files_array[@]} -eq 0 ]; then
    echo "No files named $target_file found in $script_dir"
    exit 1
elif [ ${#files_array[@]} -eq 1 ]; then
    selected_file="${files_array[0]}"
else
    echo "Multiple files found:"
    for i in "${!files_array[@]}"; do
        echo "$((i+1)). ${files_array[$i]}"
    done
    
    # 提示用户选择文件
    read -p "Enter the number of the file you want to select: " file_index
    file_index=$((file_index-1))

    if [ $file_index -ge 0 ] && [ $file_index -lt ${#files_array[@]} ]; then
        selected_file=${files_array[$file_index]}
    else
        echo "Invalid selection."
        exit 1
    fi
fi

selected_dir=$(dirname "$selected_file")
echo "Selected directory: $selected_dir"

# 查找上级目录中的 "src" 目录
src_path=$(echo "$selected_dir" | grep -o ".*/src")

if [ -z "$src_path" ]; then
    echo "No such folder named src"
    exit 1
else
    echo "Found src path: $src_path"
fi

# 检查并执行 morai_ws 的 setup.bash
if [ -d "$src_path/morai_ws" ]; then
    if [ -f "$src_path/morai_ws/devel/setup.bash" ]; then
        source "$src_path/morai_ws/devel/setup.bash"
        echo "Sourced: $src_path/morai_ws/devel/setup.bash"
    else
        echo "Please catkin make morai package"
    fi
else
    echo "No such folder named morai_ws"
fi

# 查找并处理 mobiniq 路径
mobiniq_path="$src_path/mobiniq"
if [ -d "$mobiniq_path" ]; then
    echo "Found mobiniq path: $mobiniq_path"
    export PYTHONPATH=$PYTHONPATH:"$mobiniq_path"
    echo "Exported PYTHONPATH: $PYTHONPATH"
else
    echo "No such folder named MOBINIQ"
fi

# 使用推断的 mobiniq_path 运行 Python 脚本
python3 "$mobiniq_path/selfdrive/visualize/visualize.py" 2> >(grep -v TF_REPEATED_DATA) &
sleep 3
python3 "$mobiniq_path/selfdrive/car/car.py" &
python3 "$mobiniq_path/selfdrive/control/control.py" &
python3 "$mobiniq_path/selfdrive/perception/perception.py"

