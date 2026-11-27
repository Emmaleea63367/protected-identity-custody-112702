# 受保护身份的联合核验与启封

两家保护机构分别登记本方对象和已核验的比较证明，承办组提供独立的对象引用与收件记录。比较材料是合成的可比证明，用于验证身份授权，不是实名标识。

资料中的对象、身份及记录均为虚构。各来源使用 UTF-8 JSON Lines，一行是一个原始对象。`seq` 是全局到达序号，按演练资料的可知顺序排列。事实发生时刻、确认时刻与适用时段以同行中的独立字段为准，用相对演练起点的整数分钟表达。JSON `null` 保留来源的缺省或未确认值。除非来源明确使用相同标识，编号只在所属来源和实体域内有意义。

## 来源

- `sources/objects.jsonl`　custodian 和 alias 联合定位本地对象，revision 是该对象引用修订；case 是所属案件。
- `sources/requests.jsonl`　承办申请指定两边对象及确切修订。purpose、recipient 和 release 协同界定申请。
- `sources/proofs.jsonl`　保管端返回同次比对内可比较的 token。proof 的撤回用状态变更表明，fields 是该保管端明确获准交付的属性。
- `sources/assignment.jsonl`　承办归属登记中 holder 的角色和生效时间。
- `sources/delivery.jsonl`　收件方有独立的实际接收记录，received_at 为空时仅有待办，kind 区分比较答复与停用通知。

## 查看记录

使用 Python 3.11.2 标准库，无需安装第三方包。以下命令列出可读取的来源、查看单个来源记录并检查资料格式。读取命令按输入顺序输出 JSON，可通过 `--through` 限制已到达的记录。

```bash
python3 source_records.py
python3 source_records.py objects
python3 -m unittest discover -s tests -v
```
