# 参考になった関数や処理

学習を進める中で参考になった関数や処理についてまとめていく。

## groupby

`pandas.DataFrame`を使用する際に、`groupby`で集計することがある。例えば、以下のような処理で`print`すると次のような出力となる。`sum`以外にも`min`や`max`、`mean`などで集計もできる。これ以外にも`apply`も使用できる。

```python
import pandas as pd
import random
random.seed(3407)

n = 50

fruit = random.choices(["apple", "orange", "banana"], k=n)
like = random.choices([1,2,3,4,5], k=n)
df = pd.DataFrame({"fruit":fruit, "like": like})
print(df.groupby(by="fruit").sum())

#         like
# fruit      
# apple     67
# banana    42
# orange    30
```

また、特定の`fruit`毎に別の集計したい場合は以下のように`if`で分岐を作って処理できる。

```python
for f, df_ in df.groupby(by="fruit"):
    if f=="apple":
        print(f, df_["like"].sum())
    else:
        print(f, df_["like"].mean())

# apple 67
# banana 2.625
# orange 2.5
```


## locals

ローカル変数を取得する関数。以下を実行すればよく、返り値はkeyがローカル変数名、valueがkeyのローカル変数名に対応する値の辞書。

```python
locals()
```
