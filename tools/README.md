# 完整源归档重建

本 tag 是 Mbed TLS 4.1.0 的受控 host 完整源，SDK 使用此 fork 的 master，二者不是同一源码装配。官方源与 tag、实际子来源、生成命令、冻结工具和清理/注释差异均在根 workspace-source.json。GitHub 同 network fork 复用不会更换 SDK master。

从精确 host tag 完整 clone 后执行 `git submodule update --init --recursive --checkout`，核对所有 Git 根干净，再执行 `python3 tools/package_source_archive.py --output /new/path/mbedtls-4.1.0-actions-exit.tar.bz2`。脚本递归纳入所有精确 gitlink 的 tracked 源，固定排序、执行位和零时间戳；不会下载依赖、读取 Profile、签名或部署产品。

31 个官方生成文件已提交，GEN_FILES 保持发布模式 OFF。若要核对官方生成来源，按冻结 requirements 在隔离临时环境运行 metadata 中的两次官方生成命令及 prepare_release.sh，再按 metadata 只处理已声明的生成注释差异，核对所有生成文件摘要。实际源归档SHA由正式Release资产与消费者锁冻结；本tag不声称与官方tar逐字节相同。
