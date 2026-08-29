
| case | what failed | likely cause | proposed change |
|---|------|---------|--------------|
| 002, 005, 008, 009, 012, 014, 017 | missing information | has no defined vocabulary in the instructions, so the model free-writes descriptions instead of using schema field names. | instruct model |
| 003, 004, 006 | reading customerIds | cid format| instruct model to format cids to a consistent pattern |
