
using System;
using System.Collections.Generic;

namespace IDLite
{
	public abstract class IDLiteBase
	{
		protected int ToInt(object o)
		{
			return (int)ToLong(o);
		}

		protected int? ToNullableInt(object o)
		{
			return (int?)ToNullableLong(o);
		}

		protected long ToLong(object o)
		{
			return ToNullableLong(o).Value;
		}

		protected long? ToNullableLong(object o)
		{
			if (o is long) {
				return (long)o;
			} else if (o is double) {
				return (long)(double)o;
			} else {
				return null;
			}
		}

		protected double ToDouble(object o)
		{
			return ToNullableDouble(o).Value;
		}

		public static double? ToNullableDouble(object o)
		{
			if (o is long) {
				return (double)(long)o;
			} else if (o is double) {
				return (double)o;
			} else {
				return null;
			}
		}

		protected string ToString(object o)
		{
			return ToNullableString(o);
		}

		protected string ToNullableString(object o)
		{
			if (o is string) {
				return (string)o;
			} else {
				return null;
			}
		}

		protected bool ToBool(object o)
		{
			return ToNullableBool(o).Value;
		}

		protected bool? ToNullableBool(object o)
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
	}
}
