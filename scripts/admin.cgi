#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ [ WebPatio ]
#│ admin.cgi - 2007/05/06
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
require '../scripts/init.cgi';
require $jcode;

&parse_form;
if ($in{'pass'} eq "") { &enter; }
elsif ($in{'pass'} ne $pass) { &error("認証エラー"); }
if ($in{'logfile'} || $in{'bakfile'}) { &file_mente; }
elsif ($in{'filesize'}) { &filesize; }
elsif ($in{'member'} && $authkey) { &member_mente; }
&menu_disp;

#-------------------------------------------------
#  ログメンテ
#-------------------------------------------------
sub file_mente {
	local($subject,$log,$top,$itop,$sub,$res,$nam,$em,$com,$da,$ho,$pw,$re,
		$sb,$na2,$key,$last_nam,$last_dat,$del,@new,@new2,@sort,@file,@del,@top);

	# メニューからの処理
	if ($in{'job'} eq "menu") {
		foreach ( keys(%in) ) {
			if (/^past(\d+)/) {
				$in{'past'} = $1;
				last;
			}
		}
	}

	# 汚染チェック
	$in{'no'} =~ s/[^0-9\0]//g;

	# index定義
	local($mylog);
	if ($in{'bakfile'}) {
		$log = $pastfile;
		$subject = "過去ログ";
		$mylog = "bakfile";
	} else {
		$log = $nowfile;
		$subject = "現行ログ";
		$mylog = "logfile";
	}

	# スレッド一括削除
	if ($in{'action'} eq "del" && $in{'no'} ne "") {

		# 削除情報
		local(@del) = split(/\0/, $in{'no'});

		# indexより削除情報抽出
		local($top, @new);
		open(DAT,"+< $log") || &error("Open Error: $log");
		eval "flock(DAT, 2);";
		$top = <DAT> if (!$in{'past'});
		while(<DAT>) {
			$flg = 0;
			local($no) = split(/<>/);
			foreach $del (@del) {
				if ($del == $no) {

					# ログ展開
					open(DB,"$logdir/$del.cgi");
					while( $db = <DB> ) {
						local($no,$sub,$nam,$eml,$com,$dat,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/, $db);

						# 画像削除
						foreach $i (1 .. 3) {
							next if (!$upl{$i});

							local($ex) = split(/,/, $upl{$i});
							if (-e "$upldir/$tim-$i$ex") {
								unlink("$upldir/$tim-$i$ex");
							}
						}
					}
					close(DB);

					# スレッド削除
					unlink("$logdir/$del.cgi");
					unlink("$logdir/$del.dat");
					$flg = 1;
					last;
				}
			}
			if (!$flg) { push(@new,$_); }
		}

		# index更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# スレッドのロック開閉
	} elsif ($in{'action'} eq "lock" && $in{'no'} ne "" && !$in{'past'}) {

		# ロック情報
		local(@lock) = split(/\0/, $in{'no'});

		# スレッドヘッダ情報更新
		foreach (@lock) {

			local($top,@file);
			open(DAT,"+< $logdir/$_.cgi") || &error("Open Error: $_.cgi");
			eval "flock(DAT, 2);";
			@file = <DAT>;

			$top = shift(@file);

			# 先頭記事分解、キー開閉
			local($num,$sub,$res,$key) = split(/<>/, $top);

			# 0=ロック 1=標準 2=管理用
			if ($key eq '0') { $key = 1; } else { $key = 0; }

			# スレッド更新
			unshift(@file,"$num<>$sub<>$res<>$key<>\n");
			seek(DAT, 0, 0);
			print DAT @file;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# index読み込み
		local($top,@new);
		open(DAT,"+< $log") || &error("Open Error: $log");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			s/\n//;
			local($no,$sub,$res,$nam,$da,$na2,$key,$upl) = split(/<>/);

			foreach $lock (@lock) {
				# 0=ロック 1=標準 2=管理用
				if ($lock == $no) {
					if ($key eq '0') { $key = 1; } else { $key = 0; }
					$_ = "$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>";
				}
			}
			push(@new,"$_\n");
		}

		# index更新
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# スレッドの管理者コメントモード
	} elsif ($in{'action'} eq "lock2" && $in{'no'} ne "" && !$in{'past'}) {

		# ロック情報
		local(@lock) = split(/\0/, $in{'no'});

		# スレッドヘッダ情報更新
		foreach (@lock) {

			local($top, @file);
			open(DAT,"+< $logdir/$_.cgi") || &error("Open Error: $_.cgi");
			eval "flock(DAT, 2);";
			@file = <DAT>;

			$top = shift(@file);

			# 先頭記事分解、キー開閉
			local($num,$sub,$res,$key) = split(/<>/, $top);

			# 0=ロック 1=標準 2=管理用
			if ($key < 2) { $key = 2; } else { $key = 1; }

			# スレッド更新
			unshift(@file,"$num<>$sub<>$res<>$key<>\n");
			seek(DAT, 0, 0);
			print DAT @file;
			truncate(DAT, tell(DAT));
			close(DAT);
		}

		# index読み込み
		local($top, $flg, @new, @top1, @top2);
		open(DAT,"+< $log") || &error("Open Error: $log");
		eval "flock(DAT, 2);";
		$top = <DAT>;
		while(<DAT>) {
			$flg = 0;
			s/\n//;
			local($no,$sub,$res,$nam,$da,$na2,$key,$upl) = split(/<>/);

			foreach $lock (@lock) {
				if ($lock == $no) {
					# 0=ロック 1=標準 2=管理用
					if ($key == 2) {
						$key = 1;
						$_ = "$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>";
					} else {
						$key = 2;
						push(@top1,"$no<>$sub<>$res<>$nam<>$da<>$na2<>$key<>$upl<>\n");
						$flg = 1;
					}
					last;
				}
			}
			if (!$flg) {
				if ($key == 2) {
					push(@top2,"$_\n");
				} else {
					push(@new,"$_\n");
				}
			}
		}

		# index更新
		unshift(@new,@top2) if (@top2 > 0);
		unshift(@new,@top1) if (@top1 > 0);
		unshift(@new,$top);
		seek(DAT, 0, 0);
		print DAT @new;
		truncate(DAT, tell(DAT));
		close(DAT);

	# スレッド内レス記事閲覧
	} elsif ($in{'action'} eq "view" && $in{'no'} ne "") {

		# レス記事個別削除
		if ($in{'job'} eq "del" && $in{'no2'} ne "") {

			local($top,$num,$sub2,$res,$key,$flg,@del,@new);

			if ($in{'no2'} =~ /\b0\b/) {
				&error("親記事の削除はできません");
			}

			# 削除情報を配列化
			@del = split(/\0/, $in{'no2'});

			# スレッド内より削除記事を抽出
			local($top, @new);
			open(DAT,"+< $logdir/$in{'no'}.cgi");
			eval "flock(DAT, 2);";
			$top = <DAT>;
			local($num,$sub2,$res,$key) = split(/<>/, $top);
			while(<DAT>) {
				$flg = 0;
				local($no,$sub,$nam,$em,$com,$da,$ho,$pw,$url,$mvw,$myid,$tim,$upl{1},$upl{2},$upl{3}) = split(/<>/);
				foreach $del (@del) {
					if ($no == $del) {
						$flg = 1;

						# 画像削除
						foreach $i (1 .. 3) {
							next if (!$upl{$i});

							local($ex) = split(/,/, $upl{$i});
							if (-e "$upldir/$tim-$i$ex") {
								unlink("$upldir/$tim-$i$ex");
							}
						}

						last;
					}
				}
				if (!$flg) {
					push(@new,$_);

					# 最終投稿者名と時間を覚えておく
					$last_nam = $nam;
					$last_dat = $da;
				}
			}

			# レス個数を調整
			$res -= @del;
			$top = "$num<>$sub2<>$res<>$key<>\n";

			# スレッド更新
			unshift(@new,$top);
			seek(DAT, 0, 0);
			print DAT @new;
			truncate(DAT, tell(DAT));
			close(DAT);

			# index内容差し替え
			@new2 = (); @sort = (); @top = ();
			open(DAT,"+< $log");
			eval "flock(DAT, 2);";
			$top2 = <DAT> if ($in{'past'} == 0);
			while(<DAT>) {
				s/\n//;
				local($no,$sb,$re,$na,$da,$na2,$key,$upl) = split(/<>/);

				if ($key == 2) {
					push(@top,"$_\n");
					next;
				}
				if ($in{'no'} == $no) {
					# レス個数と最終投稿者名を差替
					$na2 = $last_nam;
					$da  = $last_dat;
					$_ = "$no<>$sb<>$res<>$na<>$da<>$na2<>$key<>$upl<>";
				}
				push(@new2,"$_\n");

				# ソート用配列
				$da =~ s/\D//g;
				push(@sort,$da);
			}

			# 投稿順にソート
			@new2 = @new2[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];

			# index更新
			unshift(@new2,@top) if (@top > 0);
			unshift(@new2,$top2) if ($in{'past'} == 0);
			seek(DAT, 0, 0);
			print DAT @new2;
			truncate(DAT, tell(DAT));
			close(DAT);

		# レス記事個別修正
		} elsif ($in{'job'} eq "edit" && $in{'no2'} ne "") {

			# 複数選択の場合は先頭のみ
			($in{'no2'}) = split(/\0/, $in{'no2'});

			require $editlog;
			&edit_log("admin");
		}

		# スレッド内個別閲覧
		&header;
		print "<div align=\"right\">\n";
		print "<form action=\"$admincgi\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"admin\">\n";
		print "<input type=\"hidden\" name=\"$mylog\" value=\"1\">\n";
		print "<input type=\"submit\" value=\"&lt;&lt; 戻る\"></form></div>\n";
		print "<form action=\"$admincgi\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"pass\" value=\"$in{'pass'}\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"admin\">\n";
		print "<input type=\"hidden\" name=\"$mylog\" value=\"1\">\n";
		print "<input type=\"hidden\" name=\"no\" value=\"$in{'no'}\">\n";
		print "<input type=\"hidden\" name=\"action\" value=\"view\">\n";

		open(IN,"$logdir/$in{'no'}.cgi");
		$top = <IN>;
		($num,$sub,$res) = split(/<>/, $top);

		print "スレッド名 ： <b>$sub</b> [ $subject ]<hr>\n";
		print "<li>修正又は削除を選択して記事をチェックします。<br>\n";
		print "<li>親記事の削除はできません。<br><br>\n";
		print "処理 ： <select name=\"job\">\n";
		print "<option value=\"edit\" selected>修正\n";
		print "<option value=\"del\">削除</select>\n";
		print "<input type=\"submit\" value=\"送信する\">\n";
		print "<dl>\n";

		while (<IN>) {
			local($no,$sub,$nam,$em,$com,$da,$ho,$pw,$url,$mvw,$myid) = split(/<>/);

			if ($em) { $nam="<a href=\"mailto:$em\">$nam</a>"; }

			print "<dt><input type=\"checkbox\" name=\"no2\" value=\"$no\"> ";
			print "[<b>$no</b>] <b>$nam</b> - $da ";
			print "【<font color=\"$al\">$ho</font>】\n";

			if ($authkey) { print "ID:$myid\n"; }

			print "<dd>$com\n";
		}
		close(IN);

		print "</dl></form>\n</body></html>\n";
		exit;
	}

	&header;
	print <<"EOM";
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; 管理TOP">
</form>
<h3 style="font-size:16px">管理モード [ $subject ]</h3>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="mode" value="admin">
<input type="hidden" name="$mylog" value="1">
スレッド処理 <select name="action">
<option value="view">個別メンテ
<option value="del">スレ削除
EOM

	if ($in{'past'} == 0) {
		print "<option value=\"lock\">ロック開閉\n";
		print "<option value=\"lock2\">管理者\n";
	}

	print <<EOM;
</select>
<input type="submit" value="送信する">
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="400">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="4" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center" nowrap>選択</td>
  <td bgcolor="$col3" width="100%">&nbsp; スレッド</td>
  <td bgcolor="$col3" align="center" nowrap>レス数</td>
</tr>
EOM

	# スレッド一覧
	open(IN,"$log") || &error("Open Error: $log");
	$top = <IN> if (!$in{'bakfile'});
	while (<IN>) {
		local($no,$sub,$res,$nam,$da,$na2,$key) = split(/<>/);

		print "<tr bgcolor=\"$col2\"><th bgcolor=\"$col2\">";
		print "<input type=checkbox name=\"no\" value=\"$no\"></th>";
		print "<td bgcolor=\"$col2\">";

		if ($key eq '0') {
			print "[<font color=\"$al\">ロック中</font>] ";
		} elsif ($key == 2) {
			print "[<font color=\"$al\">管理コメント</font>] ";
		}

		print "<b>$sub</b></td>";
		print "<td bgcolor=\"$col2\" align=\"center\">$res</td></tr>\n";
	}
	close(IN);

	print <<EOM;
</table>
</Td></Tr></Table>
</form>
</body>
</html>
EOM

	exit;
}

#-------------------------------------------------
#  ファイルサイズ
#-------------------------------------------------
sub filesize {
	local($top,$tmp,$num,$all,$all2,$size1,$size2,$size3,$size4,$file,$file1,$file2);

	# 現行ログ
	$size1 = 0;
	$file1 = 0;
	open(IN,"$nowfile") || &error("Open Error: $nowfile");
	$top = <IN>;
	while (<IN>) {
		($num) = split(/<>/);
		$tmp = -s "$logdir/$num.cgi";
		$size1 += $tmp;
		$file1++;

		$now{$num} = 1;
	}
	close(IN);

	# 過去ログ
	$size2 = 0;
	$file2 = 0;
	open(IN,"$pastfile") || &error("Open Error: $pastfile");
	while (<IN>) {
		($num) = split(/<>/);
		$tmp = -s "$logdir/$num.cgi";
		$size2 += $tmp;
		$file2++;

		$pst{$num} = 1;
	}
	close(IN);

	# 画像
	opendir(DIR,"$upldir");
	local(@dir) = readdir(DIR);
	closedir(DIR);

	local($img) = 0;
	foreach (@dir) {
		next unless (/^[\d\-]+\.(jpg|gif|png)$/);

		$img += -s "$upldir/$_";
	}

	$size1 = int ($size1 / 1024 + 0.5);
	$size2 = int ($size2 / 1024 + 0.5);
	$img   = int ($img / 1024 + 0.5);
	$all = $size1 + $size2;
	$file = $file1 + $file2;

	&header;
	print <<"EOM";
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; 管理TOP">
</form>
<h3 style="font-size:16px">ログ容量算出</h3>
<ul>
<li>以下は記録ファイルの容量（サイズ）で、小数点以下は四捨五入します。
<li>分類欄のフォームをクリックすると各管理画面に移動します。
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="280">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" rowspan="2" align="center">分類</td>
  <td bgcolor="$col3" rowspan="2" width="70" align="center">ファイル数</td>
  <td bgcolor="$col3" colspan="2" align="center">サイズ</td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center" width="50">ログ</td>
  <td bgcolor="$col3" align="center" width="50">画像</td>
</tr>
<tr>
  <th bgcolor="$col2">
   <input type="submit" name="logfile" value="現行ログ"></th>
  <td align="right" bgcolor="$col2">$file1</td>
  <td align="right" bgcolor="$col2">$size1 KB</td>
  <td align="right" bgcolor="$col2" rowspan="2">$img KB</td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2">
   <input type="submit" name="bakfile" value="過去ログ"></th>
  </th>
  <td align="right" bgcolor="$col2">$file2</td>
  <td align="right" bgcolor="$col2">$size2 KB</td>
</tr>
<tr bgcolor="$col2">
  <th bgcolor="$col2">合計</th>
  <td align="right" bgcolor="$col2">$file</td>
  <td align="right" bgcolor="$col2">$all KB</td>
  <td align="right" bgcolor="$col2">$img KB</td>
</tr>
</table>
</Td></Tr></Table>
</form>
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  会員管理
#-------------------------------------------------
sub member_mente {
	# 新規フォーム
	if ($in{'job'} eq "new") {

		&member_form();

	# 新規発行
	} elsif ($in{'job'} eq "new2") {

		local($err);
		if (!$in{'name'}) { $err .= "名前が未入力です<br>\n"; }
		if ($in{'myid'} =~ /\W/) { $err .= "IDは英数字のみです<br>\n"; }
		if (length($in{'myid'}) < 4 || length($in{'myid'}) > 8) {
			$err .= "IDは英数字で4～8文字です<br>\n";
		}
		if ($in{'mypw'} =~ /\W/) { $err .= "パスワードは英数字のみです<br>\n"; }
		if (length($in{'mypw'}) < 4 || length($in{'mypw'}) > 8) {
			$err .= "パスワードは英数字で4～8文字です<br>\n";
		}
		if (!$in{'rank'}) { $err .= "権限が未選択です<br>\n"; }
		if ($err) { &error($err); }

		local($flg,$crypt,$id,$pw,$rank,$nam,@data);

		# IDチェック
		$flg = 0;
		open(DAT,"+< $memfile") || &error("Open Error: $memfile");
		while(<DAT>) {
			local($id,$pw,$rank,$nam) = split(/<>/);

			if ($in{'myid'} eq $id) { $flg = 1; last; }
			push(@data,$_);
		}

		if ($flg) { &error("このIDは既に登録済です"); }

		# パス暗号化
		$crypt = &encrypt($in{'mypw'});

		# 更新
		seek(DAT, 0, 0);
		print DAT "$in{'myid'}<>$crypt<>$in{'rank'}<>$in{'name'}<>\n";
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

	# 修正フォーム
	} elsif ($in{'job'} eq "edit" && $in{'myid'}) {

		if ($in{'myid'} =~ /\0/) { &error("修正選択は１つのみです"); }

		local($flg,$id,$pw,$rank,$nam);

		$flg = 0;
		open(IN,"$memfile") || &error("Open Error: $memfile");
		while (<IN>) {
			($id,$pw,$rank,$nam) = split(/<>/);

			if ($in{'myid'} eq $id) { $flg = 1; last; }
		}
		close(IN);

		&member_form($id,$pw,$rank,$nam);

	# 修正実行
	} elsif ($in{'job'} eq "edit2") {

		local($err,$crypt);
		if (!$in{'name'}) { $err .= "名前が未入力です<br>\n"; }
		if ($in{'myid'} =~ /\W/) { $err .= "IDは英数字のみです<br>\n"; }
		if (length($in{'myid'}) < 4 || length($in{'myid'}) > 8) {
			$err .= "IDは英数字で4～8文字です<br>\n";
		}
		if ($in{'chg'}) {
			if ($in{'mypw'} =~ /\W/) { $err .= "パスワードは英数字のみです<br>\n"; }
			if (length($in{'mypw'}) < 4 || length($in{'mypw'}) > 8) {
				$err .= "パスワードは英数字で4～8文字です<br>\n";
			}

			# パス暗号化
			$crypt = &encrypt($in{'mypw'});

		} elsif (!$in{'chg'} && $in{'mypw'} ne "") {
			$err .= "パスワードの強制変更はチェックボックスに選択してください<br>\n";
		}
		if (!$in{'rank'}) { $err .= "権限が未選択です<br>\n"; }
		if ($err) { &error($err); }

		local($flg,$id,$pw,$rank,$nam,@data);

		open(DAT,"+< $memfile") || &error("Open Error: $memfile");
		while(<DAT>) {
			local($id,$pw,$rank,$nam) = split(/<>/);

			if ($in{'myid'} eq $id) {
				if ($crypt) { $pw = $crypt; }
				$_ = "$id<>$pw<>$in{'rank'}<>$in{'name'}<>\n";
			}
			push(@data,$_);
		}

		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

	# 削除
	} elsif ($in{'job'} eq "dele" && $in{'myid'}) {

		local($flg,@data,@del);

		# 削除情報
		@del = split(/\0/, $in{'myid'});

		open(DAT,"+< $memfile") || &error("Open Error: $memfile");
		while(<DAT>) {
			local($id,$pw,$rank,$nam) = split(/<>/);

			$flg = 0;
			foreach $del (@del) {
				if ($del eq $id) { $flg = 1; last; }
			}
			if (!$flg) { push(@data,$_); }
		}

		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	&header;
	print <<"EOM";
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; 管理TOP">
</form>
<h3 style="font-size:16px">会員管理</h3>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="member" value="1">
<input type="hidden" name="past" value="3">
処理 :
<select name="job">
<option value="new">新規
<option value="edit">修正
<option value="dele">削除
</select>
<input type="submit" value="送信する">
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="280">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="3" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center" nowrap width="30">選択</td>
  <td bgcolor="$col3" align="center" nowrap>ID</td>
  <td bgcolor="$col3" align="center" nowrap>名前</td>
  <td bgcolor="$col3" align="center" nowrap>ランク</td>
</tr>
EOM

	open(IN,"$memfile") || &error("Open Error: $memfile");
	while (<IN>) {
		($id,$pw,$rank,$nam) = split(/<>/);

		print "<tr bgcolor=\"$col2\"><th bgcolor=\"$col2\">";
		print "<input type=\"checkbox\" name=\"myid\" value=\"$id\"></th>";
		print "<td bgcolor=\"$col2\" nowrap>$id</td>";
		print "<td bgcolor=\"$col2\">$nam</td>";
		print "<td bgcolor=\"$col2\" align=\"center\">$rank</td>";
	}
	close(IN);

	print <<EOM;
</table>
</Td></Tr></Table>
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  会員フォーム
#-------------------------------------------------
sub member_form {
	local($id,$pw,$rank,$nam) = @_;
	local($job) = $in{'job'} . '2';

	&header();
	print <<EOM;
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="member" value="1">
<input type="submit" value="&lt; 前画面">
</form>
<h3 style="font-size:16px">登録フォーム</h3>
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="member" value="1">
<input type="hidden" name="job" value="$job">
<Table border="0" cellspacing="0" cellpadding="0" width="350">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>名前</td>
  <td bgcolor="$col2"><input type="text" name="name" size="25" value="$nam"></td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>ログインID</td>
  <td bgcolor="$col2">
EOM

	if ($in{'myid'}) {
		print $in{'myid'};
	} else {
		print "<input type=\"text\" name=\"myid\" size=\"10\" value=\"$id\">\n";
		print "（英数字で4～8文字）\n";
	}

	print <<EOM;
  </td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>パスワード</td>
  <td bgcolor="$col2">
	<input type="password" name="mypw" size="10"> （英数字で4～8文字）
EOM

	if ($in{'myid'}) {
		print "<br><input type=\"checkbox\" name=\"chg\" value=\"1\">\n";
		print "パスワードを強制変更する場合にチェック\n";
		print "<input type=\"hidden\" name=\"myid\" value=\"$in{'myid'}\">\n";
	}

	print <<EOM;
  </td>
</tr>
<tr bgcolor="$col1">
  <td bgcolor="$col2" align="center" nowrap>権限</td>
  <td bgcolor="$col2">
EOM

	local(%rank) = (1,"閲覧のみ", 2,"閲覧&amp;書込OK");
	foreach (1,2) {
		if ($rank == $_) {
			print "<input type=radio name=rank value=\"$_\" checked>レベル$_ ($rank{$_})<br>\n";
		} else {
			print "<input type=radio name=rank value=\"$_\">レベル$_ ($rank{$_})<br>\n";
		}
	}

	print <<EOM;
  </td>
</tr>
</table>
</Td></Tr></Table>
<p>
<input type="submit" value="送信する">
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  メニュー画面
#-------------------------------------------------
sub menu_disp {
	# セッションディレクトリ掃除
	if ($authkey && $in{'login'}) {
		&ses_clean;
	}

	&header;
	print <<EOM;
<form action="$bbscgi">
<input type="submit" value="&lt; 掲示板">
</form>
<div align="center">
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="job" value="menu">
処理内容を選択してください。
<p>
<Table border="0" cellspacing="0" cellpadding="0" width="320">
<Tr><Td bgcolor="$col1">
<table border="0" cellspacing="1" cellpadding="5" width="100%">
<tr bgcolor="$col1">
  <td bgcolor="$col3" align="center">
	選択
  </td>
  <td bgcolor="$col3" width="100%">
	&nbsp; 処理内容
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" align="center">
	<input type="submit" name="logfile" value="選択">
  </td>
  <td bgcolor="$col2" width="100%">
	&nbsp; 現行ログ・メンテナンス
  </td>
</tr>
<tr bgcolor="$col2">
  <td bgcolor="$col2" align="center">
	<input type="submit" name="bakfile" value="選択">
  </td>
  <td bgcolor="$col2" width="100%">
	&nbsp; 過去ログ・メンテナンス
  </td>
</tr>
EOM

	if ($authkey) {
		print "<tr bgcolor=\"$col2\"><td bgcolor=\"$col2\" align=\"center\">\n";
		print "<input type=\"submit\" name=\"member\" value=\"選択\"></td>";
		print "<td bgcolor=\"$col2\" width=\"100%\">&nbsp; 会員認証の管理</td></tr>\n";
	}

	print <<EOM;
<tr bgcolor="$col2">
  <td bgcolor="$col2" align="center">
	<input type="submit" name="filesize" value="選択">
  </td>
  <td bgcolor="$col2" width="100%">
	&nbsp; ファイル容量の閲覧
  </td>
</tr>
</table>
</Td></Tr></Table>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  入室画面
#-------------------------------------------------
sub enter {
	&header;
	print <<EOM;
<blockquote>
<table border="0" cellspacing="0" cellpadding="26" width="400">
<tr><td align="center">
	<fieldset>
	<legend>
	▼管理パスワード入力
	</legend>
	<form action="$admincgi" method="post">
	<input type="hidden" name="login" value="1">
	<input type="password" name="pass" size="16">
	<input type="submit" value=" 認証 "></form>
	</fieldset>
</td></tr>
</table>
</blockquote>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  セションディレクトリ掃除
#-------------------------------------------------
sub ses_clean {
	local($mtime,@dir);

	opendir(DIR,"$sesdir");
	@dir = readdir(DIR);
	closedir(DIR);

	foreach (@dir) {
		next unless (/^\w+\.cgi$/);

		$mtime = (stat("$sesdir/$_"))[9];
		if (time - $mtime > $authtime*60*2) {
			unlink("$sesdir/$_");
		}
	}
}

