history_vector = None


def calculate_score(reference_vector, current_vector, distance, confidence, img_w, img_h):
    """
    计算综合评分
    评分 = 方向匹配度 + 距离评分 + 置信度评分
    
    参数:
        reference_vector: 参考向量 (dx, dy)
        current_vector: 当前目标向量 (dx, dy)
        distance: 距离
        confidence: 置信度
        img_w, img_h: 图像尺寸
    
    返回:
        float: 综合评分
    """
    import math

    # 1. 方向匹配度 (0-1，越接近1越好)
    if reference_vector is not None:
        # 计算两个向量的点积
        dot_product = reference_vector[0] * current_vector[0] + reference_vector[1] * current_vector[1]
        
        # 计算向量长度
        len_ref = math.sqrt(reference_vector[0]**2 + reference_vector[1]**2)
        len_cur = math.sqrt(current_vector[0]**2 + current_vector[1]**2)
        
        if len_ref > 0 and len_cur > 0:
            # 计算余弦值，范围[-1, 1]
            cos_angle = dot_product / (len_ref * len_cur)
            # 转换为[0, 1]范围，1表示完全同向
            direction_score = (cos_angle + 1) / 2
        else:
            direction_score = 0.5  # 默认中等分数
    else:
        direction_score = 0.5  # 没有参考向量时给中等分数
    
    # 2. 距离评分 (0-1，越近越好)
    max_distance = math.sqrt((img_w/2)**2 + (img_h/2)**2)  # 图像对角线的一半
    # 归一化距离到[0,1]范围，然后反转（距离越近评分越高）
    normalized_distance = min(distance / max_distance, 1.0)  # 限制最大值为1
    distance_score = 1 - normalized_distance
    
    # 3. 置信度评分 (0-1，越高越好)
    conf_score = confidence
    
    # 4. 综合评分 (权重: 方向0.6, 距离0.25, 置信度0.15)
    total_score = 0.1 * direction_score + 0.8 * distance_score + 0.1 * conf_score
    
    return total_score



def get_target_vector(results, image_size, min_conf=0.5, reference_vector=None):
    """
    根据YOLO检测结果，使用综合评分选择最佳目标。
    评分 = 方向匹配度 + 距离评分 + 置信度评分

    参数:
        results: YOLO模型的检测结果（单张图片），通常为results[0]
        image_size: 截图的尺寸 (width, height)
        min_conf: 最低置信度阈值
        reference_vector: 参考向量 (dx, dy)，用于方向匹配

    返回:
        dict 或 None, 例如:
        {
            "center": (x, y),  # 目标中心点坐标
            "cls": 类别索引,
            "conf": 置信度,
            "distance": 距离图像中心的欧氏距离,
            "score": 综合评分
        }
        如果没有目标，返回None
    """
    # 提取边界框、类别和置信度
    boxes = results.boxes.xyxy  # (x1, y1, x2, y2)
    classes = results.boxes.cls
    confidences = results.boxes.conf

    # 图像中心点坐标
    img_w, img_h = image_size
    center_x, center_y = img_w / 2, img_h / 2

    # 用于存储符合条件的目标
    candidates = []

    for i, box in enumerate(boxes):
        conf = float(confidences[i])
        if conf < min_conf:
            continue  # 跳过置信度低的目标

        # 计算目标中心点
        x1, y1, x2, y2 = box.tolist()
        obj_cx = (x1 + x2) / 2
        obj_cy = (y1 + y2) / 2

        # 计算与图像中心的欧氏距离
        dist = ((obj_cx - center_x) ** 2 + (obj_cy - center_y) ** 2) ** 0.5

        # 计算当前目标向量
        current_vector = (obj_cx - center_x, obj_cy - center_y)
        
        # 计算综合评分
        score = calculate_score(reference_vector, current_vector, dist, conf, img_w, img_h)

        # 保存目标信息
        candidates.append({
            "center": (obj_cx, obj_cy),
            "cls": int(classes[i]),
            "conf": conf,
            "distance": dist,
            "score": score
        })

    if not candidates:
        # 没有符合条件的目标
        return None

    # 按综合评分排序，评分最高的排在前面
    candidates.sort(key=lambda x: -x["score"])

    # 返回评分最高的目标
    return candidates[0]





# 新增函数：返回截图中心到目标的向量（dx, dy）
def get_center_to_target_vector(results, image_size, min_conf=0.5, reference_vector=None):
    """
    计算截图中心到目标中心的向量(dx, dy)，使用综合评分选择最佳目标
    
    参数:
        results: 检测结果（与get_target_vector一致）
        image_size: (宽, 高)
        min_conf: 最小置信度
        reference_vector: 参考向量 (dx, dy)，用于方向匹配
    
    返回:
        (dx, dy): 截图中心指向目标中心的向量
        如果没有目标，返回None
    """
    global history_vector
    if reference_vector is None:
        reference_vector = history_vector
    history_vector = reference_vector

    # 步骤1：调用get_target_vector获取最佳目标
    target = get_target_vector(results, image_size, min_conf, reference_vector)
    if target is None:
        return None  # 没有目标

    # 步骤2：获取截图中心点
    img_w, img_h = image_size
    center_x, center_y = img_w / 2, img_h / 2

    # 步骤3：获取目标中心点
    obj_cx, obj_cy = target["center"]

    # 步骤4：计算向量（目标中心 - 截图中心）
    dx = obj_cx - center_x
    dy = obj_cy - center_y

    history_vector = (dx, dy)
    # 步骤5：返回向量
    return (dx, dy)


