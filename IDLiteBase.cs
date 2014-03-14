
using System;
using System.Collections.Generic;

namespace IDLite
{
	public abstract class IDLiteBase
	{
		protected int ParseInt(object o)
		{
			return (int)ParseLong(o);
		}

		protected int? ParseNullableInt(object o)
		{
			return (int?)ParseNullableLong(o);
		}

		protected long ParseLong(object o)
		{
			return ParseNullableLong(o).Value;
		}

		protected long? ParseNullableLong(object o)
		{
			if (o is long) {
				return (long)o;
			} else if (o is double) {
				return (long)(double)o;
			} else {
				return null;
			}
		}

		protected double ParseDouble(object o)
		{
			return ParseNullableDouble(o).Value;
		}

		public static double? ParseNullableDouble(object o)
		{
			if (o is long) {
				return (double)(long)o;
			} else if (o is double) {
				return (double)o;
			} else {
				return null;
			}
		}

		protected string ParseString(object o)
		{
			return ParseNullableString(o);
		}

		protected string ParseNullableString(object o)
		{
			if (o is string) {
				return (string)o;
			} else {
				return null;
			}
		}

		protected bool ParseBool(object o)
		{
			return ParseNullableBool(o).Value;
		}

		protected bool? ParseNullableBool(object o)
		{
			if (o is bool) {
				return (bool)o;
			} else {
				return null;
			}
		}

		protected static List<T> GetList<T>(Dictionary<string, object> dict, string name, Func<object, T> func)
		{
			if (dict.ContainsKey(name) && dict[name] is List<object>) {
				var a = new List<T>();
				foreach (var x in (List<object>)dict[name]) {
					a.Add(func(x));
				}
				return a;
			}
			return null;
		}

		protected static object GetItem(Dictionary<string, object> dict, string name)
		{
			if (dict.ContainsKey(name)) {
				return dict[name];
			} else {
				return null;
			}
		}

		protected static List<object> SerializeList<T>(List<T> list) where T : IDLiteBase
		{
			var a = new List<object>();
			foreach (var x in list) {
				a.Add(x.Serialize());
			}
			return a;
		}

		public abstract Dictionary<string, object> Serialize();
	}
}
