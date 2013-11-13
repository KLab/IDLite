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
using System;
using System.Collections.Generic;
using UnityEngine;

[Serializable]
public partial class Ball
{
	public string id;
	public double x;
	public double y;
	public int z;
	public Dictionary<string, object> obj;
	public List<Dictionary<string, object>> objects;

	public Ball(string id, double x, double y, int z, Dictionary<string, object> obj, List<Dictionary<string, object>> objects)
	{
		this.id = id;
		this.x = x;
		this.y = y;
		this.z = z;
		this.obj = obj;
		this.objects = objects;
	}

	public Ball(Dictionary<string, object> dict)
	{
		object _o;
		if (dict.TryGetValue("id", out _o))
		{
			id = (string)_o;
		}
		else
		{
			Debug.Log("id not found");
		}
		if (dict.TryGetValue("x", out _o))
		{
			x = (double)_o;
		}
		else
		{
			Debug.Log("x not found");
		}
		if (dict.TryGetValue("y", out _o))
		{
			y = (double)_o;
		}
		else
		{
			Debug.Log("y not found");
		}
		if (dict.TryGetValue("z", out _o))
		{
			z = (int)_o;
		}
		dict.TryGetValue("obj", out obj);
		objects = new List<Dictionary<string, object>>();
		if (dict.TryGetValue("objects", out _o))
		{
			foreach (var _v in (List<object>)_o)
			{
				objects.Add((Dictionary<string, object>)_v);
			}
		}
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

	public Player(Dictionary<string, object> dict)
	{
		object _o;
		if (dict.TryGetValue("id", out _o))
		{
			id = (int)_o;
		}
		else
		{
			Debug.Log("id not found");
		}
		if (dict.TryGetValue("name", out _o))
		{
			name = (string)_o;
		}
		else
		{
			Debug.Log("name not found");
		}
		balls = new List<Ball>();
		if (dict.TryGetValue("balls", out _o))
		{
			foreach (var _v in (List<object>)_o)
			{
				balls.Add(new Ball((Dictionary<string, object>)_v));
			}
		}
	}
}
```
