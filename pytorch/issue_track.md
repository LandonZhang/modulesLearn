1. `detach()` -> 此参数不需要记录梯度,为纯粹的数值

- (在 PyTorch 中，如果输入张量需要梯度，那么基于它的计算结果也会自动需要梯度)

2. `AvgPool1d()`

- 平均池化 (Average Pooling) 是一种下采样操作，通过在滑动窗口内计算平均值来减少序列长度，同时保留重要信息。
- `kernel_size` 表示采样多少数据进行均值计算
- `stride` 表示步长
- `padding` 表示在边界数字左右填充多少个 0 (默认方式就是 0 填充) -> 确保边界位置的数字也能通过继承周围数字来正确平均化

3. `ReplicationPad1d()`

- nn.ReplicationPad1d 是一个一维复制填充层
- 它通过复制边界值来对输入张量进行填充
- 可以自定义左边界或者右边界的数据复制多少次

4. `torch.Tensor.unfold`

- dimension: 要展开的维度
- size: 每个窗口的大小
- step: 窗口之间的步长

5. `nn.ModuleList()`

- `method_to_use: `append, insert, expand
- 自动参数注册：所有子模块的参数都会被正确注册（并且使用  `state_dict()`时，名称自动命名：head_layers.0.weight, head_layers.1.weight）
- 设备管理：调用 .to(device) 时会自动移动所有子模块
- 训练模式：调用 .train()/.eval() 时会自动设置所有子模块
- 参数优化：优化器能够找到所有需要训练的参数

6. `nn.Flatten()`

- 把多维张量“拉直”成二维张量，方便送入全连接层
- 可以自定义起始维度和结束维度

7. `nn.Dropout()`

- 随机隐去一部分结果（设置为 0），提升模型的泛化能力
- 训练时: 随机将部分神经元输出置零，强迫网络不依赖特定神经元
- 预测时: 使用所有神经元
- 注意: 被保留的神经元输出会按 1/(1-p) 缩放以保持期望值不变（丢掉 50% 的值，剩下的值会被放大两倍）

8. `nn.init()`

- 用于将 tensor 中的空值（0值）使用一定的方式填充

9. `torch.Tensor.masked_fill()`

- masked_fill 函数用于根据掩码条件将张量中的特定位置填充为指定值
- 语法: `tensor.masked_fill_(mask, value)`
- mask: 布尔类型张量，True 的位置会被填充
- value: 要填充的值
- 带下划线的版本是就地操作，不带下划线的版本返回新张量

