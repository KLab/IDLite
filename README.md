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
}

class Player {
    int id
    string name
    List<Ball> balls  # List<T> は、 JSON の [] の各要素を、T に deserialize します.
}
```

### 生成されるコード

```cs
[Serializable]
public partial class Ball
{
	public string id;
	public double x;
	public double y;

	public Ball(string id, double x, double y)
	{
		this.id = id;
		this.x = x;
		this.y = y;
	}

	public static Ball FromDict(Dictionary<string, object> dict)
	{
		var id = dict.GetValue<string>("id");
		var x = dict.GetValue<double>("x");
		var y = dict.GetValue<double>("y");
		return new Ball(id, x, y);
	}
}

[Serializable]
public partial class Player
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

	public static Player FromDict(Dictionary<string, object> dict)
	{
		var id = dict.GetValue<int>("id");
		var name = dict.GetValue<string>("name");
		var balls = new List<Ball>();
		foreach (var o in dict.GetValue<List<object>>("balls"))
		{
			balls.Add(Ball.FromDict((Dictionary<string, object>)o));
		}
		return new Player(id, name, balls);
	}
}

```
