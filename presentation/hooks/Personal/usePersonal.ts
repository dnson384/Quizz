"use client";
import { UpdateUser } from "@/domain/entities/User";
import { useAuthContext } from "@/presentation/context/auth.context";
import {
  updateMe,
  uploadTempAvatar,
} from "@/presentation/services/user.service";
import { usePathname, useRouter } from "next/navigation";
import React, { useEffect, useState, useRef } from "react";
import { isAxiosError } from "axios";

export default function usePersonal() {
  const router = useRouter();
  const pathname = usePathname();

  const { user } = useAuthContext();

  // Error
  const [error, setError] = useState<string | null>(null);

  // Upload Ảnh
  const [newAvatar, setNewAvatar] = useState<string>();
  const [uploading, setUploading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Update Data
  const [updateData, setUpdateData] = useState<UpdateUser>();

  // Redirect Edit
  const handleEditClick = () => {
    router.push(`${pathname}/edit`);
  };

  // Upload ảnh
  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];
    await handleUploadAvatar(file);
  };

  const handleUploadAvatar = async (file: File) => {
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const newAvatarUrl = await uploadTempAvatar(formData);
      setNewAvatar(newAvatarUrl);
      setUpdateData((prev) => {
        if (!prev) return prev;
        return { ...prev, avatarUrl: newAvatarUrl };
      });
    } catch (err) {
      if (isAxiosError(err)) {
        const newErr = err.response?.data.detail;
        setError(newErr);
      }
    } finally {
      setUploading(false);
    }
  };

  // Input Change
  const handleFieldChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const target = event.target;
    const { name, value } = target;
    setUpdateData((prev) => {
      if (!prev) return prev;

      const currentKey = name as keyof typeof user;
      if (user && user[currentKey] === value) return prev;

      return { ...prev, [name]: value };
    });
  };

  // Save
  const handeSaveChangeClick = async (formValid: boolean) => {
    if (!updateData) return;
    const valid = Object.entries(updateData).some(([key, value]) => {
      if (key === "id") return false;
      const currentKey = key as keyof typeof user;
      if (user && user[currentKey] === value) return false;
      if (value !== null) return true;
    });

    if (valid && formValid) {
      if (!confirm("Xác nhận thay đổi")) return;
      try {
        const response = await updateMe(updateData);
        if (response.data) {
          window.location.reload();
        }
      } catch (err) {
        if (isAxiosError(err)) {
          const newErr = err.response?.data.detail;
          setError(newErr);
        }
      }
    } else {
      setError("Dữ liệu thay đổi không hợp lệ");
    }
  };

  const handleCancelChange = () => {
    router.push("/personal");
  };

  useEffect(() => {
    if (user) {
      setUpdateData({
        id: user.id,
        name: null,
        email: null,
        role: null,
        avatarUrl: null,
      });
    }
  }, [user]);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  return {
    error,
    user,
    newAvatar,
    fileInputRef,
    uploading,
    updateData,
    handleFileChange,
    handleButtonClick,
    handleEditClick,
    handleFieldChange,
    handeSaveChangeClick,
    handleCancelChange,
  };
}
