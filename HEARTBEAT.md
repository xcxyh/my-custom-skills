# HEARTBEAT.md

## Daily Check-in

每天检查用户是否超过24小时没发消息。如果是，主动联系。

状态文件：memory/heartbeat-state.json

检查逻辑：
1. 读取 memory/heartbeat-state.json，获取 lastMessageTime
2. 如果当前时间 - lastMessageTime > 24小时，发送消息
3. 发送后更新 lastContactTime

## 学习与成长 (每 8-12 小时)

状态文件：memory/heartbeat-state.json

检查逻辑：
1. 读取 memory/heartbeat-state.json，获取 lastLearningCheck
2. 如果当前时间 - lastLearningCheck > 8小时，执行以下：
   - 整理 memory/YYYY-MM-DD.md，提取重要信息到 MEMORY.md
   - 更新 MEMORY.md，删除过时信息
   - 记录学到的新技能或洞察到 memory/learning-log.md
3. 更新 lastLearningCheck

## 主动性任务 (每 2-3 小时)

状态文件：memory/heartbeat-state.json

检查逻辑：
1. 读取 memory/heartbeat-state.json，获取 lastProactiveCheck
2. 如果当前时间 - lastProactiveCheck > 2小时，执行以下：
   - 检查是否有新工具或技能值得学习
   - 记录潜在改进点
3. 更新 lastProactiveCheck

## 记忆维护 (每 3-5 天)

定期整理和优化记忆：

检查逻辑：
1. 读取 memory/heartbeat-state.json，获取 lastMemoryMaintenance
2. 如果当前时间 - lastMemoryMaintenance > 3天，执行以下：
   - 遍历 memory/*.md 文件
   - 提取重要事件、决策、学到的东西
   - 更新 MEMORY.md
   - 删除过期的临时信息
   - 压缩重复内容
3. 更新 lastMemoryMaintenance
