# 完整源归档重建

`darren-you/reference-host-mbedtls` 是 ESP FRP Host 的独立完整受控来源，保留 Mbed TLS 4.1.0 和 TF-PSA-Crypto 1.1.0 的实际源码与版本。正式来源是本仓 `master` 中经 PR 合并的精确提交；SDK 来源继续由 `darren-you/reference-sdk-mbedtls` 的独立 `master` 管理。官方源、实际子来源、生成命令、冻结工具和差异均在根 `workspace-source.json`。

先完整 clone 本仓并 checkout 所选精确提交，再执行 `git submodule update --init --recursive --checkout`。核对根仓及所有子来源的原始 tracked 字节、对象与 gitlink 完整匹配，且不存在任何未跟踪内容（包括 ignored 文件），然后执行：

```bash
python3 tools/package_source_archive.py --output "/new/path/mbedtls-4.1.0-actions-exit-$(git rev-parse HEAD).tar.bz2"
```

文件名包含实际运行时的完整 40 位 Host 提交 SHA。脚本递归纳入所有精确 gitlink 的 tracked 源，固定排序、执行位和零时间戳；输出路径必须是新路径。正式 `v4.1.0` Release 资产与消费者锁使用真实合并提交及实际归档 SHA-256，验证中的候选提交不能冒充后续合并提交。包器不下载依赖、读取 Profile、签名或部署产品。

31 个官方生成文件已提交，`GEN_FILES` 保持发布模式 `OFF`。若要核对官方生成来源，按冻结 requirements 在隔离临时环境运行 metadata 中的两次官方生成命令及 `prepare_release.sh`，仅处理已声明的生成注释差异，并核对所有生成文件摘要。metadata 的官方 Git/发布包文件计数是初始官方来源比较的记录，不是当前受控归档总文件数。

TFPSA gitlink 使用其正式 `master` 合并提交 `e9014b46d32b0a152a4e451e65e0a7af89939f75`。该提交只调整文档 CMake 接线：作为子工程时不向源码目录写入文档配置，独立工程仍保留原有文档配置与目标。TLS/PSA 的运行 C、头文件和汇编源码，以及31个生成文件摘要保持不变；这里不声明文档 HTML 渲染已经执行，也不声明受控归档与官方 tar 逐字节相同。
