#��������������������������������������������������������������������
#�� [ WebPatio ]
#�� upload.pl - 2007/06/30
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �A�b�v���[�h
#-------------------------------------------------
sub upload {
	local($no) = @_;
	local(@ret);

	foreach $i (1 .. 3) {

		if (!defined($uplno{$i})) {
			push(@ret,("","",""));
			next;
		}

		local($w,$h);

		# Content-Type�w�b�_����t�@�C����ނ�F��
		local($ex);
		if ($ctype{$i} =~ m|image/gif|i) {
			$ex = '.gif';
		} elsif ($ctype{$i} =~ m|image/p?jpeg|i) {
			$ex = '.jpg';
		} elsif ($ctype{$i} =~ m|image/png|i) {
			$ex = '.png';
		}

		# Content-Type�ł͕s���̂Ƃ��͊g���q����t�@�C����ނ�F��
		if (!$ex) {
			if ($fname{$i} =~ /\.gif$/) {
				$ex = '.gif';
			} elsif ($fname{$i} =~ /\.jpe?g$/) {
				$ex = '.jpg';
			} elsif ($fname{$i} =~ /\.png$/) {
				$ex = '.png';
			}
		}

		# �t�@�C���F���ł����Ƃ��͏�������
		if ($ex) {
			local($upfile) = $in{"upfile$i"};

			# �}�b�N�o�C�i���r��
			if ($macbin) {
				local($len) = substr($upfile, 83, 4);
				$len = unpack("%N", $len);
				$upfile = substr($upfile, 128, $len);
			}

			# �A�b�v�t�@�C����`
			local($imgfile) = "$upldir/$no-$i$ex";

			# ��������
			open(OUT,">$imgfile") || &error("�摜�A�b�v���s");
			binmode(OUT);
			print OUT $upfile;
			close(OUT);

			# �p�[�~�b�V�����ύX
			chmod(0666, $imgfile);

			# �摜�T�C�Y�擾
			if ($ex eq ".jpg") { ($w,$h) = &j_size($imgfile); }
			elsif ($ex eq ".gif") { ($w,$h) = &g_size($imgfile); }
			elsif ($ex eq ".png") { ($w,$h) = &p_size($imgfile); }
		}
		# ��������
		push(@ret,($ex,$w,$h));
	}
	# �Ԃ�l
	return @ret;
}

#-------------------------------------------------
#  JPEG�T�C�Y�F��
#-------------------------------------------------
sub j_size {
	local($jpeg) = @_;
	local($t, $m, $c, $l, $W, $H);

	open(JPEG, "$jpeg") || return (0,0);
	binmode JPEG;
	read(JPEG, $t, 2);
	while (1) {
		read(JPEG, $t, 4);
		($m, $c, $l) = unpack("a a n", $t);

		if ($m ne "\xFF") {
			$W = $H = 0;
			last;
		} elsif ((ord($c) >= 0xC0) && (ord($c) <= 0xC3)) {
			read(JPEG, $t, 5);
			($H, $W) = unpack("xnn", $t);
			last;
		} else {
			read(JPEG, $t, ($l - 2));
		}
	}
	close(JPEG);
	return ($W, $H);
}

#-------------------------------------------------
#  GIF�T�C�Y�F��
#-------------------------------------------------
sub g_size {
	local($gif) = @_;
	local($data);

	open(GIF,"$gif") || return (0,0);
	binmode(GIF);
	sysread(GIF,$data,10);
	close(GIF);

	if ($data =~ /^GIF/) { $data = substr($data,-4); }

	$W = unpack("v",substr($data,0,2));
	$H = unpack("v",substr($data,2,2));
	return ($W, $H);
}

#-------------------------------------------------
#  PNG�T�C�Y�F��
#-------------------------------------------------
sub p_size {
	local($png) = @_;
	local($data);

	open(PNG, "$png") || return (0,0);
	binmode(PNG);
	read(PNG, $data, 24);
	close(PNG);

	$W = unpack("N", substr($data, 16, 20));
	$H = unpack("N", substr($data, 20, 24));
	return ($W, $H);
}



1;

