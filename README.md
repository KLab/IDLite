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
// コメントは無視されます。 (TODO: コメントをコード生成に反映させる)
// ボール

enum Color {
    red = 1,
    green = 2,
    blue = 3
};

class Ball {
    string owner;
    enum Color color;
    float x; # x座標.
    float y;
};
```

### 生成されるコード

```cs
// This code is automatically generated.
// Don't edit this file directly.
using System;
using System.Collections.Generic;

namespace IDLite
{
	public enum Color
	{
		red = 1,
		green = 2,
		blue = 3
	}

	[Serializable]
	public class Ball : IDLiteBase
	{
		public string owner;
		public Color color;
		public double x;
		public double y;

		public Ball(string owner, Color color, double x, double y)
		{
			this.owner = owner;
			this.color = color;
			this.x = x;
			this.y = y;
		}

		public Ball(Dictionary<string, object> dict)
		{
			this.owner = ToString(GetItem(dict, "owner"));
			this.color = (Color)ToInt(GetItem(dict, "color"));
			this.x = ToDouble(GetItem(dict, "x"));
			this.y = ToDouble(GetItem(dict, "y"));
		}
	}

}
```
