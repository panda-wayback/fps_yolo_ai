# 目标选择器 (Target Selector)

根据YOLO识别结果选择目标的模型。

## 功能特性

- 支持多种选择策略：距离中心最近、最高置信度等
- 可配置最小置信度阈值
- 自动过滤不符合条件的目标
- 提供选中目标的详细信息（中心点、边界框、置信度、类别ID）

## 使用方法

### 基本使用

```python
from data_center.models.target_selector.subject import TargetSelectorSubject
from data_center.models.yolo_model.subject import YoloSubject

# 1. 获取YOLO检测结果
yolo_state = YoloSubject.get_yolo_model_state()
if yolo_state.yolo_results:
    # 2. 发送检测结果给目标选择器
    TargetSelectorSubject.send_yolo_results(yolo_state.yolo_results)
    
    # 3. 获取选择结果
    selector_state = TargetSelectorSubject.get_state()
    if selector_state.selected_target:
        print(f"选中目标中心点: {selector_state.selected_target}")
        print(f"目标边界框: {selector_state.target_bbox}")
        print(f"目标置信度: {selector_state.target_confidence}")
        print(f"目标类别ID: {selector_state.target_class_id}")
```

### 配置参数

```python
# 方法1：使用配置接口设置
TargetSelectorSubject.set_config(
    distance_weight=0.3,      # 距离权重
    confidence_weight=0.4,    # 置信度权重
    similarity_weight=0.2,    # 相似度权重
    class_weight=0.1,         # 类别权重
    reference_vector=(100, 200)  # 参考向量
)

# 方法2：部分更新配置
TargetSelectorSubject.set_config(
    distance_weight=0.5,
    confidence_weight=0.5
)

# 方法3：直接修改状态（不推荐）
selector_state = TargetSelectorSubject.get_state()
selector_state.distance_weight = 0.3
```

## 配置参数说明

- `distance_weight`: 距离权重 (0-1)，距离屏幕中心越近权重越高
- `confidence_weight`: 置信度权重 (0-1)，置信度越高权重越高
- `similarity_weight`: 相似度权重 (0-1)，与参考向量越相似权重越高
- `class_weight`: 类别权重 (0-1)，特定类别权重
- `reference_vector`: 参考向量 (x, y)，用于计算相似度

## 状态字段

- `selected_point`: 选中目标的中心点坐标 (x, y)
- `selected_bbox`: 选中目标的边界框 (x1, y1, x2, y2)
- `selected_confidence`: 选中目标的置信度
- `selected_class_id`: 选中目标的类别ID
- `distance_weight`: 距离权重
- `confidence_weight`: 置信度权重
- `similarity_weight`: 相似度权重
- `class_weight`: 类别权重
- `reference_vector`: 参考向量
