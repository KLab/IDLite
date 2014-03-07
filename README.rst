IDLite
======

IDLite は開発中のプロジェクトです。
予告なく、下位互換性のない変更を行います。

背景
-----

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

サンプル
---------

IDL
^^^^

.. code-block:: cpp

    // ドキュメントコメント
    // 複数行書けます.
    enum Color {
        red = 1,
        green = 2,
        blue = 3
    };

    # 無視されるコメント

    // ボール
    class Ball {
        // ボールの持ち主
        string? owner;
        // ボールの色
        enum Color color;
        // 座標
        float x;
        float y;
    };

    class Field {
        List<Ball> balls;
    };


生成されるコード
^^^^^^^^^^^^^^^^

.. code-block:: c#

    // This code is automatically generated.
    // Don't edit this file directly.
    using System;
    using System.Collections.Generic;

    namespace IDLite
    {
            /// <summary>
            /// ドキュメントコメント
            /// 複数行書けます.
            /// </summary>
            public enum Color
            {
                    red = 1,
                    green = 2,
                    blue = 3
            }


            /// <summary>
            /// ボール
            /// </summary>
            [Serializable]
            public partial class Ball : IDLiteBase
            {
                    /// <summary>
                    /// ボールの持ち主
                    /// </summary>
                    public string owner;
                    /// <summary>
                    /// ボールの色
                    /// </summary>
                    public Color color;
                    /// <summary>
                    /// 座標
                    /// </summary>
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

            [Serializable]
            public partial class Field : IDLiteBase
            {
                    public List<Ball> balls;

                    public Field(List<Ball> balls)
                    {
                            this.balls = balls;
                    }

                    public Field(Dictionary<string, object> dict)
                    {
                            this.balls = GetList<Ball>(dict, "balls", (object o) => { return new Ball((Dictionary<string, object>)o); });
                    }
            }

    }
