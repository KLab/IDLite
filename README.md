# IDLite

IDLite は開発中のプロジェクトです。
予告なく、下位互換性のない変更を行います。

## 背景

IDLite は、 Unity でモバイルオンラインゲームを作成するときに、 Unity C# で JSON を
扱うのが面倒なのを解決してくれるツールです。

固い protocol を使いたい場合は　protocol buffer や thrift や msgpack idl がありますが、
これらは効率的にデータをパックするために、 {"キー": 値} という構造ではなくて、
配列中の位置に意味をもたせているため、効率よりも Web 系のカジュアルな開発スタイルを
重視する場合には使いにくいことがあります。

JSON schema もありますが、これも複雑で学習が難しいものです。

LitJSON など、 JSON を手軽に扱える C# のライブラリはありますが、
リフレクションやジェネリクスに制限のある iOS では動かないケースがあります。

IDLite は、この隙間の需要を満たすためのものです。

## サンプル

### IDL

```
# コメントは無視されます。 (TODO: コメントをコード生成に反映させる)
# ボール
class Ball {
    string id
    float x  # x座標.
    float y
    int? z
    object obj
    List<object> objects
}

class Player {
    int id
    string name
    List<Ball> balls  # List<T> は JSON の [] に割り当てられますが、その要素が T にパースされます.
}
```

### 生成されるコード

```cs
// This code is automatically generated.
// Don't edit this file directly.
using System;
using System.Collections.Generic;

namespace IDLite
{
	[Serializable]
	public class Ball : IDLiteBase
	{
		public string id;
		public double x;
		public double y;
		public int? z;

		public Ball(string id, double x, double y, int? z)
		{
			this.id = id;
			this.x = x;
			this.y = y;
			this.z = z;
		}

		public Ball(Dictionary<string, object> dict)
		{
			this.id = ToString(GetItem(dict, "id"));
			this.x = ToDouble(GetItem(dict, "x"));
			this.y = ToDouble(GetItem(dict, "y"));
			this.z = ToNullableInt(GetItem(dict, "z"));
		}
	}

	[Serializable]
	public class Player : IDLiteBase
	{
		public int id;
		public string name;
		public List<Ball> balls;

		public Player(int id, string name, List<Ball> balls)
		{
			this.id = id;
			this.name = name;
			this.balls = balls;
		}

		public Player(Dictionary<string, object> dict)
		{
			this.id = ToInt(GetItem(dict, "id"));
			this.name = ToString(GetItem(dict, "name"));
			this.balls = GetList<Ball>(dict, "balls", (object o) => { return new Ball((Dictionary<string, object>)o); });
		}
	}

}
```
